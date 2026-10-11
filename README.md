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
7. Save settings. Optionally load available model IDs after saving the keys.
8. Click **Test saved settings**; then upload documents.

Claude, Pinecone inference, and index operations incur usage charges in your provider accounts. The app does not provision or purchase a Pinecone index.

### Pinecone setup

Create an ordinary **dense vector index**, using **cosine** similarity and **1024 dimensions** for the default `multilingual-e5-large` model. Do not use an integrated text-record index for this implementation: Folio explicitly generates embeddings and upserts vectors. Copy the data-plane host from the Pinecone dashboard.

The embedding and reranking endpoints use the same Pinecone API key. Defaults are `multilingual-e5-large` and `bge-reranker-v2-m3`. Claude's default is `claude-sonnet-4-6`. Model IDs are editable, and **Load models** queries your accounts. Availability depends on provider access and lifecycle. Test settings before ingestion. If you change embedding models, the index dimension must match; changing the vector space requires deleting and re-ingesting the documents.

## Settings fallback from `.env`

Missing or blank saved fields fall back to backend environment variables, then built-in defaults. The backend loads the project-root `.env` on startup without overriding existing process environment variables. Nonempty saved settings take priority.

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

Provider keys persist on the backend. The browser stores only the chosen endpoint URL in localStorage. The workspace token is held in React memory and needs re-entry after a page refresh. Disconnect clears the token and loaded settings. Network errors include guidance for HTTPS and CORS.

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
