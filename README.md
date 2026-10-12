# Folio — FastAPI + React document intelligence

Upload documents, generate summaries and metadata with Claude, index dense vectors in Pinecone, and search using lexical BM25, vector retrieval, hybrid RRF, and optional model reranking.

## Run locally

Install Docker with Compose and Python 3. Run these commands from the extracted project folder:

```sh
python setup.py
docker compose up --build
```

Open **http://localhost:5173**. The interface initially shows a clearly labeled sample workspace. Sample search is a simple keyword demonstration, not the live retrieval engine.

1. Open **Settings → Workspace connection**.
2. Enter `http://localhost:8000` as the backend URL.
3. Copy `APP_TOKEN` from your generated `.env` file into the workspace token field. Keep that token private.
4. Click **Connect backend**.
5. Enter your **Claude API key** and **Pinecone API key**.
6. Enter the Pinecone **index host** and choose a dedicated namespace.
7. Set CLAUDE_MODEL, EMBEDDING_MODEL, and RERANK_MODEL in .env; restart the backend. Save provider settings.
8. Click **Test saved settings**; then upload documents.

Claude, Pinecone inference, and index operations incur usage charges in your provider accounts. The app does not provision or purchase a Pinecone index.

### Pinecone setup

Create an ordinary **dense vector index**, using **cosine** similarity and **1024 dimensions** for the `multilingual-e5-large` model in `.env.example`. Do not use an integrated text-record index for this implementation: Folio explicitly generates embeddings and upserts vectors. Copy the data-plane host from the Pinecone dashboard.

The embedding and reranking endpoints use the same Pinecone API key. Model selections come exclusively from the required environment variables in `.env`: `CLAUDE_MODEL` (summaries, metadata, HyDE, ticket decisions and DSPy workflow), `EMBEDDING_MODEL` (ingestion and retrieval), and `RERANK_MODEL`. Settings displays these values read-only. There are no model defaults or saved model overrides. Startup fails with a clear error if any is missing. Docker receives these variables through its `.env` env_file. Restart the backend after changing them. Changing the embedding model requires a matching index dimension and deleting/re-ingesting existing documents.

## Provider settings

Non-model settings retain their saved-setting/environment behavior. Model configuration is exclusively environment-based. Use `.env.example` as the configuration template.

```env
CLAUDE_API_KEY=your-claude-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_HOST=your-index.svc.region.pinecone.io
PINECONE_NAMESPACE=folio
CLAUDE_MODEL=claude-sonnet-4-6
EMBEDDING_MODEL=multilingual-e5-large
RERANK_MODEL=bge-reranker-v2-m3
```

Lowercase field names such as `claude_key`, `pinecone_key`, `index_host`, and `namespace` are also supported. `ANTHROPIC_API_KEY`, `CLAUDE_KEY`, `PINECONE_KEY`, `INDEX_HOST`, and `NAMESPACE` are aliases. The uppercase names in the example take priority over aliases. Restart the backend after changing `.env`. Blank key inputs in the UI preserve saved keys or continue using the environment fallback; fallback keys are never returned to the browser or copied into saved settings merely by saving unrelated fields.

## What is included

- React interface: documents, upload modal, ingestion activity, document details, summaries, metadata, searchable summary inspection, original download, deletion, search playground, and settings.
- FastAPI backend with generated OpenAPI docs at `http://localhost:8000/docs` (click Authorize and enter APP_TOKEN).
- Persistent SQLite records, full-text index, encrypted provider settings, and original files in the Docker `folio-data` volume.
- A durable SQLite job queue processed by one background worker. In-progress jobs restart after a backend restart. Failed jobs stay visible and can be retried.
- Content hashing prevents duplicate ingestion. Stable vector IDs make ingestion retries overwrite existing vectors rather than creating duplicates.
- SHA-based duplicate detection is scoped to this single workspace. Different filenames with identical bytes resolve to the existing document.
- New documents have one searchable summary and one vector. Summaries describe the whole document and do not claim a source page.
- Document deletion removes explicit vector IDs from Pinecone, then the local searchable entries, record, and original file. It fails visibly if Pinecone deletion fails.
- API keys are encrypted at rest using Fernet and never returned by the API. The encryption key is stored in a restricted file in the same persistent volume. This protects database-only exposure, not a fully compromised host or volume.
- APP_TOKEN protects all application routes; the unauthenticated health endpoint reveals no workspace data.

## Ingestion

```text
Upload -> durable queue -> full-text extraction -> Claude summary + metadata
       -> one summary embedding -> vector upsert + local BM25 on the summary
```

Supported input: **PDF, DOC, DOCX, Markdown, TXT, CSV, JSON, HTML, and RTF**. DOC parsing uses `antiword`, included in the Docker image. DOCX includes table text in document order; HTML scripts and styles are stripped. CSV and JSON are ingested as text, not interpreted as structured databases.

Limits: 10 uploads per request, 20 MB per file, 200 PDF pages, 400,000 extracted characters, and 50 MB expanded DOCX content. Scanned/image-only PDFs require OCR before ingestion; encrypted PDFs must be unlocked. Empty, malformed, and unsupported documents produce visible errors.

The full extracted document is sent in one Claude request, without chunking or section summaries. The summary describes **About the document** (subject and purpose) and **Main content** (key points, findings, and conclusions), in about 150-200 words and at most 2,000 characters. That summary alone is embedded and indexed for lexical, vector, hybrid, and reranked search. Original files remain available for download. If the selected model cannot accept the full document, ingestion fails visibly; the input is not silently split or truncated.

Existing indexed documents are not automatically changed. Delete and upload them again to use summary indexing. The storage/API fields named `chunks` and `chunk_count` remain compatible; a new document has one summary entry with no page citation and `indexing_mode: document_summary`. Legacy chunk settings are ignored. Embeddings retain the provider's end-truncation setting, so the chosen model's token limit still applies to a summary.

Tags, title, language, and document type are model-generated and should be reviewed for important use cases. Source text is treated as untrusted input, and the model has no action tools.

Provider requests have timeouts and up to three attempts for transient failures. After permanent failure, retry from the pipeline screen. Failed or partially indexed documents are excluded from search. Pinecone is eventually consistent; vector results may take a short time to appear after an upload is marked indexed.

## Retrieval

| Option | Implementation |
|---|---|
| Lexical | SQLite FTS5 BM25 on document summaries; query tokens joined with OR |
| Vector | Pinecone dense query embedding and index query |
| Hybrid | Reciprocal rank fusion, k=60, over BM25 and dense candidates |
| Reranking | Optional Pinecone-hosted cross-encoder over retrieved candidate text |
| Filters | Document and exact metadata tag |
| Controls | 1–20 final results; 5–100 API candidates; UI presets 20, 30, 50, 100 |

HyDE is optional and off by default. For vector or hybrid search, Claude generates a hypothetical document summary, which is embedded as a passage to retrieve real indexed documents. Hybrid lexical matching and reranking keep the original query. Generated text is not stored or presented as a source. HyDE adds a Claude call, latency, and provider usage charges. It is unavailable in lexical/sample search; generation failures are reported explicitly.

Reranking is an optional second stage on any retrieval mode. Candidate count must be at least final result count. Search results show source file, document summary (or legacy page/entry), tags, retrieval source, and score type. BM25, cosine similarity, RRF, and reranking scores are not interchangeable or calibrated confidence percentages.

Only ready documents are searched. Hybrid and rerank failures are explicit errors, never silently disguised as successful full retrieval. The current scope is retrieval of document summaries; a generated question-answering/chat stage is not included.

## Use the hosted React interface

The hosted site provides the React UI and a labeled sample workspace. **It does not host Python.** Deploy the included FastAPI container to your own Python/container host behind HTTPS, with a persistent volume mounted at `/data`, one worker, and your APP_TOKEN environment variable. Set `CORS_ORIGINS` to the exact hosted frontend origin:

```env
CORS_ORIGINS=https://folio-document-search.kartiks.chatgpt.site
```

For both local and hosted interfaces, use a comma-separated list. Restart the backend after changing environment variables. Enter the HTTPS API URL and token in Settings. HTTPS pages should use HTTPS APIs; browser mixed-content/private-network restrictions can prevent a hosted page reaching localhost. Use the Docker-hosted local interface for local development.

By default Compose binds only to localhost. For a remote deployment, explicitly configure your TLS reverse proxy/ingress and networking. Configure request-size limits to suit batch uploads (up to 200 MB across 10 files). Never put provider keys into a Vite environment variable or frontend build.

Provider keys persist on the backend. The browser stores only the chosen endpoint URL in localStorage. The workspace token defaults to VITE_APP_TOKEN at frontend build time and remains editable in Settings. Disconnect clears the token and loaded settings. Network errors include guidance for HTTPS and CORS.

## Develop without Docker

Python 3.12 and Node 22.13+ are recommended.

```sh
python setup.py
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r backend/requirements.lock.txt
# uvicorn[standard] includes python-dotenv for --env-file
uvicorn backend.main:app --env-file .env --reload --port 8000
```

Run the React app in another terminal:

```sh
npm install
npm run dev
```

If working in the full hosted Sites source checkout instead of the portable bundle, use `npx vite --config frontend/vite.config.ts` for the standalone frontend. The root hosted build retains its Sites/Vinext integration.

Install `antiword` separately for DOC outside Docker. The local API stores data in `./data` unless `DATA_DIR` is set. The Docker backend runs as an unprivileged user with a named volume. Back up both `folio.db`, the uploads directory, and `.encryption-key` together; do not commit them.

## Tests and verification

```sh
pip install pytest
python -m pytest backend/tests -q
npm run build
```

Backend integration tests exercise real FastAPI routing, SQLite FTS5, encryption, auth, ingestion, duplicate detection, failed-state exclusion, retries, deletion, filters, hybrid fusion, reranking index mapping, and file parsers. External provider responses are mocked; no live provider calls were executed during development because credentials were not supplied. Frontend TypeScript and both hosted and standalone builds are checked. Browser visual QA and a Docker build were not available in the build environment.

## Deployment scope

This is a single-owner application foundation. Run **one Uvicorn worker and one backend replica**: queue coordination intentionally uses a single embedded worker. Horizontal deployment requires an external database and job queue with atomic claims. It is not a multi-user/RBAC system, and it does not provide antivirus, OCR, user account management, audit logging, or a hardened document parser sandbox. Keep it behind private access for untrusted upload scenarios. The vector namespace should be dedicated to this workspace.

## API outline

- `GET /health`
- `GET, PUT /api/settings`
- `POST /api/settings/test` (uses the saved settings; embedding and reranking checks incur minimal inference usage)
- `GET /api/models`
- `GET, POST /api/documents`
- `GET, DELETE /api/documents/{id}`
- `GET /api/documents/{id}/download`
- `POST /api/documents/{id}/retry`
- `POST /api/search`

Provider references:
- https://platform.claude.com/docs/en/api/messages/create
- https://docs.pinecone.io/reference/api/2025-10/inference/generate-vectors
- https://docs.pinecone.io/reference/api/2025-10/inference/rerank
- https://docs.pinecone.io/reference/api/2025-10/data-plane/query


## Live workflow (LangGraph + DSPy)

The **Live workflow** tab starts with your query; an incident/session record is created automatically. Optional store, asset, and customer context can be added before starting. LangGraph executes the actual orchestration, and DSPy typed `Predict` modules perform classification, checklist planning, and feedback assessment using the configured Claude model. The source policy is `backend/escalation_procedure.md`. Existing incident JSON can still be loaded through **Import incident**.

SQLite now stores related `stores`, `users`, `assets`, `tickets`, append-only `ticket_history`, `ticket_labels`, and `ticket_workflow` records. Ticket submitters link to stable user IDs, assets link to stores, and foreign keys are enforced. Additional directory fields from the supplied schema are preserved in JSON payloads; the expandable directory editor supports stores, users, assets, and evaluation labels. Evaluation labels are never supplied to the assistant as ground truth. Tickets retain the supplied external JSON shape.

Workflow:

1. Start with a query, or open a saved workflow. DSPy classifies intent, immediate escalation triggers, exclusions, impact priority, and overrides against the supplied procedure.
2. Immediate triggers route to the local L2 queue before troubleshooting, with missing checklist information requested in parallel. Otherwise, retrieval uses actual indexed tags matching ticket category/subcategory/tags, or your explicit tag filter. When no matching metadata tags exist, a broad search is explicitly recorded in the trace.
3. The assistant reuses cached sources. It can refine retrieval or read original text from an already retrieved document, with at most four retrieval/planning hops per pass and two feedback-triggered replans before asking for clarification. Original text is read in bounded windows on demand without changing ingestion, creating chunks, or embedding extra records. Technical steps require valid source references. Sources and hop traces are inspectable.
4. The full ordered checklist is visible, with a pointer to the active step. A real LangGraph `interrupt()` pauses execution for feedback on that step. Submitting feedback resumes it with `Command(resume=...)`, automatically assesses the result, then advances to the next step, refines retrieval, or checks escalation eligibility. Record what happened and minutes actually spent. Outcomes, user replies, decisions, priority justification, and information updates are timestamped in ticket history. Proposed steps are never automatically recorded as completed. After all checks fail, the graph checks the mandatory information and 15-minute requirement, then escalates automatically once the procedure allows it. Skipped checks are not treated as completed. A newer query can supersede a pending proposal when circumstances change.
5. Routine L2 escalation requires complete mandatory information, consulted knowledge sources, and at least 15 confirmed troubleshooting minutes. Resolution requires the user's explicit confirmation and resolution notes. Immediate trigger precedence follows the supplied flow diagram.
6. Escalation creates a local L2 assignment and an email draft, including P1 on-call and customer-escalation manager routing. **No email or Slack messages are sent.** Copy the draft into your approved communication tool. Monitoring actions record customer waits, L2 acknowledgement, customer updates, and SLA breaches. The SLA panel recalculates on manual Refresh; it is not a background notification scheduler.

The SLA table is authoritative: P1 response 15 minutes, P2 1 hour, P3 3 hours, P4 8 business hours. This resolves the procedure's inconsistent P2 example. P4 uses 07:00-23:00 IST, every day; five business days is 80 business hours. Documented customer waits pause active SLA time. Priority overrides stack in listed order, bounded at P1/P4; explicit payment failure/all-POS outage remains P1. Peak hours use the ticket's reported opening time in IST. The supplied procedure's review date has passed; a support owner should review its operational rules before production adoption.

Ticket assistance uses Claude and, for vector/hybrid retrieval, Pinecone. It incurs normal provider charges. Automated tests use the real graph and SQLite checkpointer with mocked model decisions, plus typed DSPy adapter tests. A development classification was also verified with the configured Claude provider. Model classification and real-world troubleshooting outcomes are not guaranteed by automated tests. Provider failures are surfaced rather than inventing a successful answer.

API additions: `GET/POST /api/tickets`, `GET /api/tickets/{id}`, `POST /api/tickets/{id}/query`, `POST /api/tickets/{id}/confirm`, `PUT /api/tickets/{id}/information`, `POST /api/tickets/{id}/monitor`, `GET /api/tickets/procedure`, and `GET/PUT /api/ticket-directory/{stores|users|assets|labels}`. Mutating ticket requests carry the current `version`; queries also carry a unique `request_id` to prevent duplicate processing.


### Durable live execution

`data/workflow-checkpoints.sqlite` stores LangGraph checkpoints, separate from the incident records/history in `data/folio.db`. Each session has a stable `live:WF-...` thread ID. Refreshing, disconnecting, or restarting the API does not lose its checklist or current feedback interrupt. Keep both databases when backing up. Checkpoint state contains workflow data, not provider API keys.

The browser consumes an authenticated NDJSON response from `POST /api/live/start`, `/api/live/{id}/query`, `/api/live/{id}/feedback`, or `/api/live/{id}/resume`. Events report running nodes and state snapshots. This is an active request stream, not polling; `/api/documents` remains manual-refresh only. On disconnection the current run finishes to a checkpoint. Refresh restores it through `GET /api/live/{id}`. If a model or retrieval node fails, use **Resume saved operation** to retry that node; completed graph nodes are not rerun. Duplicate starts and stale feedback are guarded.

Graph: `classify -> retrieve <-> plan -> prepare -> interrupt -> feedback -> evaluate -> next step / retrieve / escalation gate -> escalate or resolve`. Immediate triggers shortcut to escalation. DSPy uses typed signatures and a chat adapter; it is not an optimized/trained program, and no optimizer training is implied. Email/Slack notifications remain drafts, and SLA monitoring is manual.


## Asset and store directory

Import the relational CSV data with `python -m backend.import_directory datas` after the database has been initialized. The importer validates duplicate IDs and store relationships, then upserts `stores.csv` into `stores` and `assets.csv` into `assets` in one transaction. All CSV columns are retained in each table's JSON payload; `asset_id` and `store_id` provide the SQL relationships. Re-importing updates records without duplicating them.

Start a Live workflow using the issue description and either a Store ID or Asset ID. A store-only workflow does not guess the affected asset. Store and equipment details are resolved from the directory, included in classification/planning, and used to contextualize retrieval. An unknown asset is rejected before creating a workflow. Refreshing/resuming retrieves current directory details. Customer identity and a full address still need confirmation when required; store support phone is not assumed to be the reporting customer's number.


## Workflow agent tools

The workflow uses actual DSPy Tool wrappers for `create_ticket`, `update_ticket`, `update_checklist`, `get_ticket`, `lookup_asset`, `lookup_store`, and `list_store_assets`. DSPy extracts explicit user facts with supporting quotes; validated tool calls save them into ticket/checklist fields. Store IDs supplied in queries or feedback are resolved against the directory and reflected in the escalation checklist. Tool changes are checkpointed, recorded in history, and applied once during projection; they cannot mark steps completed or bypass escalation/resolution gates.

Authenticated agents can discover JSON tool schemas at `GET /api/agent/tools` and invoke them at `POST /api/agent/tools/{name}`. Reads take an `arguments` object; ticket reads also require `ticket_id`. Updates require `ticket_id`, current `version`, and `arguments` (optimistic locking rejects stale updates). Example:

```json
{"ticket_id":"WF-example","version":3,"arguments":{"information":{"store_id":"SW-0001","contact_phone":"user-confirmed-number"}}}
```

Send that body to `/api/agent/tools/update_checklist`. `update_ticket` takes `arguments.fields`; `create_ticket` takes `arguments.ticket_data` matching the ticket schema and an explicit unique ticket ID. Duplicate IDs are rejected. Directory facts are read-only in the checklist; the store support phone is kept separate from the reporting user's phone.


## MLflow logs, traces and golden datasets

Start the local tracking server with `python -m backend.mlflow_server`. Open **http://localhost:5000**, experiment **folio-workflows**. Docker Compose starts a persistent MLflow service automatically. SQLite tracking data and artifacts are stored in `data/mlflow.db` and `data/mlflow-artifacts` locally, or the `mlflow-data` Docker volume.

Set `MLFLOW_ENABLED=true`, `MLFLOW_TRACKING_URI`, and `MLFLOW_EXPERIMENT_NAME` in `.env`. Each workflow query, feedback or checkpoint resume creates a run with model IDs, timings, outcome metrics, `logs/events.json`, and `workflow/result.json`. Nested spans show LangGraph nodes, DSPy model decisions, retrieval, embedding and agent tools. Traces contain sanitized inputs/outputs and errors, with ticket/session and checkpoint identifiers. Provider credentials and workspace tokens are redacted. Telemetry outages do not stop workflow execution. Tracing starts with new operations; previous executions are not reconstructed. Ingestion and search also emit traces. Supported DSPy usage data is attached to model spans; cost estimates are not invented.

`VITE_APP_TOKEN` prefills the frontend workspace token. Rebuild/restart Vite after changing it; Docker passes this variable as a frontend build argument. The default is embedded in the browser bundle as requested.

Provide reviewed golden cases as JSONL using `evaluation/golden_workflow.example.jsonl` as a template. Include a unique case ID, query, store/asset context, optional feedback turns, and expected classification, priority, escalation decision, relevant document IDs, tool calls, checklist updates and troubleshooting steps. Remove the example-only tag after reviewing labels. The template is not ground truth and is not imported automatically.

Import your reviewed cases with:

```sh
python -m backend.import_golden datas/golden_workflow.jsonl
# Update an existing dataset:
python -m backend.import_golden datas/golden_workflow.jsonl --dataset-id DATASET_ID
```

This creates a native MLflow GenAI evaluation dataset. Importing a dataset does not run evaluations or train/optimize DSPy. Evaluation/scorers can be added once the reviewed expectations and acceptance criteria are available.


## Procedure and document revisions

The active escalation procedure is stored in `data/folio.db`, in `procedure_versions` and `procedure_heads`. The Markdown file seeds version 1 only when the database is first initialized. Later file edits do not replace the database procedure. Open **Live workflow ? Procedure** to inspect history, create a revision, and activate it for new workflows. Revisions are immutable; restoring old text means creating a new revision from it. Existing tickets and checkpoints retain their `procedure_ref` (ID, version, SHA256). Tickets created before this feature are marked `assigned_on_upgrade`; their earlier decisions cannot be retroactively attributed to a known procedure version.

The authenticated API supports `GET /api/procedures`, `GET /api/procedures/{version}`, and `POST /api/procedures` with `expected_version`, `text`, and `note`. Saving atomically creates and activates the next version; stale edits return 409. Procedure editing changes model guidance. Deterministic SLA timers, priority overrides, required fields, and escalation gates are implemented in Python and require corresponding code changes when those rules change.

`PROCEDURE_CACHE_TTL=1h` enables an explicit Anthropic **one-hour prompt cache** on the stable procedure prefix. `5m` is also supported. Each cache hit refreshes its TTL. The procedure block precedes DSPy signature instructions and variable ticket context, so classification, planning, information capture, and feedback share the prefix. A new procedure revision has a different prefix. DSPy response caching stays disabled: every decision still uses the current ticket and feedback. Provider cache minimums and eviction rules still apply. MLflow's `model.usage` contains cache creation/read counters. Legacy ticket model calls also include the cached procedure block, but their differing tool schemas can yield separate caches.

`document_versions` stores document lineage, revision number, content SHA256, ingestion/model metadata, and a summary snapshot. Reupload changed bytes under the **same exact filename** to create the next revision. Identical bytes remain a duplicate and do not create or activate a revision. Renamed content is treated as a separate lineage unless its bytes already exist. Prior revisions keep their original files and summaries. Default retrieval uses the latest **ready** revision per lineage; pending/failed revisions do not hide an earlier working revision. Explicit document-ID searches can inspect a previous revision. Existing workflows may reuse their earlier cited evidence until they fetch again.

Open a document's details to browse versions, or call `GET /api/documents/{document_id}/versions`. Deleting a revision removes its original and searchable entries but retains its audit snapshot/checksum and deletion timestamp; the newest remaining ready revision becomes searchable. Existing ingested documents are backfilled without reembedding. Newly indexed vectors, search results, workflow evidence/checkpoints, and MLflow workflow artifacts carry revision references. Existing Pinecone vectors are resolved through the local document-version mapping when retrieved. Back up `folio.db`, `workflow-checkpoints.sqlite`, and `uploads/` together to retain original sources and execution history.


### One trace per ticket

Ticket creation, queries, feedback, resume, and standalone ticket tools now share one MLflow run and one trace. The root is named `ticket.<ticket_id>`; each operation appears below it, with nested graph/model/retrieval/tool spans. `data/ticket-traces.sqlite` persists the run ID, trace ID, parent span ID, and turn counter across API restarts. Include this file in backups. Identity is scoped to the tracking server and experiment. Human waiting time is included in the cumulative root timeline; operation spans show execution duration.

The root is a cumulative snapshot of the ticket, not a permanently open process-local span. Inspect `ticket_status` for the incident state and `last_operation_status` plus child span errors for execution failures. Completed operations leave the run FINISHED (or FAILED on errors); later turns append to that same run. Token/cache usage remains on each `dspy.predict` span. Per-turn logs, model configuration, and results are retained under `logs/turns/` and `workflow/turns/`; `logs/events.json` and `workflow/result.json` show the latest operation.

Existing historical traces are preserved. New ticket traces are tagged `trace_layout=ticket`; filter the MLflow Traces table with `tags.trace_layout = 'ticket'` to view the new grouping. Continuing a pre-upgrade ticket starts its cumulative trace from that point. Non-ticket operations such as standalone document ingestion or search remain separate traces.


### Model context and personal information

Workflow calls now use an explicit troubleshooting field allowlist. Customer names, telephone/email details, exact addresses, staff contacts, serial numbers, arbitrary ticket history, and resolution notes are excluded. The model sees contact-presence flags for checklist reasoning, operational asset/store information, relevant symptoms, confirmed actions, and retrieved evidence. Information extraction receives a smaller identity/technical context. Original contact details remain in the local ticket database and checkpoints for user-facing operations.

A local masking layer processes workflow context, cached procedure text, outbound provider JSON (including embedding/reranking inputs), and MLflow telemetry. It masks known personal-field values when repeated in other text, email/phone patterns, explicitly labeled names/addresses, long identifiers, links, and recognized credentials. Known personal values are scoped to each operation, not shared between customers. Provider authentication headers continue to carry their required credentials. No external PII detection service is called.

Explicitly labeled contacts such as `My name is Jane Doe. Phone: +91-98765-43210.` are captured locally; model-proposed contact-field updates are ignored. For ambiguous personal information, use the structured checklist fields. This is deterministic masking, not a guarantee of recognizing every name/address in arbitrary prose or source documents. Original files and local checkpoints intentionally retain source data. Previously exported MLflow records or data already sent to providers are not retroactively sanitized by this change.

The frontend connects once on startup using `VITE_APP_TOKEN` and the saved backend URL, or `VITE_BACKEND_URL` (localhost defaults to port 8000). Connection failures open Settings for correction. Document updates remain manual; automatic connection does not enable polling. Vite values are build-time settings; restart Vite or rebuild Docker after changing them.


## Retrieval score cutoffs and model limits

All provider model IDs and generation limits are configured in `.env`. The backend validates required values at startup; missing/invalid values fail clearly instead of using code defaults. Restart the backend after changing them. Existing `.env` deployments must add the new settings from `.env.example`. API keys retain their existing saved-settings/environment behavior.

| Setting | Current initial value | Purpose |
| --- | --- | --- |
| `CLAUDE_MODEL` | Your existing model ID | Summary, HyDE, and workflow model |
| `EMBEDDING_MODEL` | Your existing model ID | Pinecone embeddings |
| `RERANK_MODEL` | Your existing model ID | Pinecone reranking |
| `CLAUDE_SUMMARY_MAX_TOKENS` | `2200` | Document enrichment output limit |
| `CLAUDE_HYDE_MAX_TOKENS` | `600` | Hypothetical document output limit |
| `CLAUDE_WORKFLOW_MAX_TOKENS` | `15000` | DSPy decision output limit |
| `CLAUDE_LEGACY_MAX_TOKENS` | `2200` | Legacy ticket assistant output limit |
| `PROVIDER_TIMEOUT_SECONDS` | `90` | Provider/DSPy request timeout |
| `PROVIDER_MAX_ATTEMPTS` | `3` | Maximum direct HTTP attempts, including the first |
| `WORKFLOW_MODEL_MAX_RETRIES` | `1` | DSPy retries after the first attempt |
| `WORKFLOW_RETRIEVAL_TOP_K` | `5` | Workflow result count |
| `WORKFLOW_RETRIEVAL_CANDIDATES` | `30` | Workflow retrieval pool |
| `WORKFLOW_RETRIEVAL_RERANK` | `false` | Enable workflow reranking |

Maximum token values are output ceilings, not required generation lengths; they must also be supported by the selected provider/model. No temperature is forced because the configured Claude model may not support it. Provider protocol fields and adapter selection remain implementation details.

The Search playground has a **Minimum score** input. Leave it blank to use the relevant environment default; an explicit value overrides the default for that search. The workflow always uses the environment defaults. Thresholds are inclusive (`score >= cutoff`) and apply to the **final ranking score**, after reranking when enabled and before the response is returned. Rejected results are not supplied as new workflow evidence. Original excerpts survive another retrieval only when their parent document still passes; cached live-workflow evidence is checked against current defaults before reuse. If every candidate is rejected, retrieval returns an empty list without lowering the threshold or retrying unfiltered.

| Setting | Initial value | Applied to |
| --- | --- | --- |
| `RETRIEVAL_VECTOR_MIN_SCORE` | `0.5` | Vector similarity without reranking |
| `RETRIEVAL_RERANK_MIN_SCORE` | `0.3` | Final reranker score, in any retrieval mode |
| `RETRIEVAL_BM25_MIN_SCORE` | `0` | Lexical BM25 without reranking |
| `RETRIEVAL_RRF_MIN_SCORE` | `0.01` | Hybrid rank-fusion score without reranking |

These are relevance scores, **not calibrated confidence probabilities**. BM25 is query-dependent and unbounded; RRF uses small rank-based values (with the current two lists and k=60, its maximum is about 0.0328). A 0.7 similarity threshold must not be copied to RRF. Vector thresholds assume a similarity-oriented index such as the existing cosine index. Defaults are starting points, not evaluated guarantees; tune each on reviewed queries and relevant/irrelevant examples. To apply a reranker cutoff to hybrid workflow retrieval, set `WORKFLOW_RETRIEVAL_RERANK=true` and tune `RETRIEVAL_RERANK_MIN_SCORE`.

Example API request: `POST /api/search` with `{"query":"printer offline","mode":"vector","rerank":false,"min_score":0.7}`. Omit `min_score` (or pass null) for the server default. Responses include `min_score` and `score_type`, including empty results. Negative/nonfinite thresholds are rejected; non-BM25 thresholds must be at most 1. Workflow retrieval traces include the effective cutoff and score type.

Workflow output validation: `WORKFLOW_OUTPUT_MAX_RETRIES=2` allows two automatic regenerations after DSPy rejects a malformed or schema-invalid decision (at most three output-generation attempts). This is separate from provider/network retries and can incur an additional model charge. Values 0?3 are accepted; 0 disables output retries. Output still must pass the typed schema; exhausted retries preserve the checkpoint. Restart the backend after changing this setting.


Workflow response provenance and ticket context:
- New DSPy decisions and troubleshooting steps require source citations, a 0?1 confidence estimate, and a short rationale. The UI shows confidence as a percentage explicitly labeled ?model estimate?; it is not a calibrated probability or retrieval similarity score. Existing responses without metadata display ?not recorded?; scores are never invented retroactively.
- Citation IDs must belong to the pinned procedure version, current ticket facts, or supplied retrieved evidence. Technical troubleshooting steps cite retrieved documents or the pinned procedure for its standard L1 instructions. ID validation does not prove that every claim is entailed by a source. Model decision metadata is saved in the ticket workflow/checkpoint and shown under Sources & graph trace.

Live workflow structured output: DSPy uses a JSON adapter and sends Claude a native `output_config.format` JSON schema for classification, planning, feedback and information extraction. Unsupported schema bounds are removed only from the provider schema; Pydantic still enforces them locally. There is no prompt-only fallback. The versioned procedure cache prefix and credential filtering are preserved. Validation retries are controlled by `WORKFLOW_OUTPUT_MAX_RETRIES=2`; transport retries remain separately controlled by `WORKFLOW_MODEL_MAX_RETRIES`. Rejected attempts log a safe reason code (schema/JSON, support metadata, or step citations), never raw prompts or responses. Exhaustion preserves the checkpoint and reports the attempt count. Retries incur provider usage; schema enforcement does not guarantee factually correct advice or citations.

Workflow context now includes actual store/contact details, asset and store records, escalation checklist, and ticket history in Claude prompts. The added question-memory/suppression layer has been removed: the model and procedure determine clarifications, without automatic question rewriting or skipping. Existing saved question-memory records are ignored. Credentials remain excluded from model context; MLflow traces/logs still mask PII and secrets. General document/search provider requests retain their existing privacy filtering.

Planning clarification limit: `WORKFLOW_PLANNING_MAX_QUESTIONS=2` permits at most two clarification turns per ticket (set to 1 for one). Each turn asks one question. The count persists across checkpoints, resumes and new queries; older recorded answers count toward the limit. After the limit, the agent proceeds with supported troubleshooting steps, including when the user answered ?don?t know?. Step-result confirmations and mandatory escalation requirements remain separate. If no supported step exists, the workflow stops for L1 review instead of inventing instructions or entering another planning-question loop. Actual store/contact context remains available to the model.

When clarification is unavailable (for example, "I don't know"), planning moves to the applicable standard procedure immediately. Planning includes the original issue, complete stored ticket history, all confirmed outcomes and the earlier plan. If model planning yields no step, the app reuses pending earlier steps or offers the unattempted basic troubleshooting bullets from Step 2 of the pinned procedure, with procedure citations. Deterministic procedure steps do not receive invented model confidence scores.
