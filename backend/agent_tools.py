"""Validated DSPy tools shared by the graph and authenticated external agents."""
import copy
import json
import dspy
from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field

TICKET_FIELDS={'subject','description','category','subcategory','tags'}


def registry(W, ticket=None, persist=False):
    def commit(changes, checklist):
        if ticket is None: raise HTTPException(422,'Select a ticket before updating it.')
        if ticket['status'] in ('Resolved','Closed'): raise HTTPException(409,'This ticket is resolved. Start another ticket.')
        updated=copy.deepcopy(ticket)
        if checklist: W.apply_information(updated,changes)
        else:
            if not changes or set(changes)-TICKET_FIELDS: raise HTTPException(422,'Only subject, description, category, subcategory and tags can be updated by this tool. Use update_checklist for customer/store details.')
            values=W.Ticket.model_validate({**updated,**changes}).model_dump(mode='json')
            for key in changes: updated[key]=values[key]
        name='update_checklist' if checklist else 'update_ticket'
        if persist:
            if not checklist: updated['workflow'].setdefault('external_ticket_updates',{}).update(changes)
            if updated['status']=='Escalated': W.escalate(updated,'Ticket details updated. Review the notification draft.')
            updated=W.save(updated,ticket['version'],[('Agent tool',name+': '+json.dumps(changes))])
        ticket.clear();ticket.update(updated)
        return {'ticket_id':ticket['ticket_id'],'updated':changes,'version':ticket.get('version')}

    def create_ticket(ticket_data: dict) -> dict:
        """Create an Open ticket with a caller-supplied unique ticket_id and directory asset_id or store_id. Never mark an incident resolved or escalated."""
        body=W.Ticket.model_validate(ticket_data)
        if body.status!='Open' or body.escalation_flag or body.resolution_notes: raise HTTPException(422,'Create an Open ticket; workflow gates control escalation and resolution.')
        data=body.model_dump(mode='json');W.hydrate_asset(data,required=True)
        return W.create(W.Ticket.model_validate(data))

    def update_ticket(fields: dict) -> dict:
        """Update the selected ticket's subject, description, category, subcategory or tags. Cannot alter status, history, priority or step completion."""
        return commit(fields,False)

    def update_checklist(information: dict) -> dict:
        """Save user-reported checklist facts, including store_id, asset_id, customer/contact and diagnostic details. Resolve directory relationships. Never guess values or mark troubleshooting steps complete."""
        return commit(information,True)

    def get_ticket() -> dict:
        """Read the selected ticket and its current checklist, evidence and workflow state."""
        if ticket is None: raise HTTPException(422,'Select a ticket first.')
        return copy.deepcopy(ticket)

    def lookup_asset(asset_id: str) -> dict:
        """Look up an asset and its related store, version, make and model from the directory."""
        return W.asset_details(asset_id)

    def lookup_store(store_id: str) -> dict:
        """Look up verified store details by store_id."""
        return W.store_details(store_id)

    def list_store_assets(store_id: str) -> list[dict]:
        """List assets belonging to a store. Never choose an affected asset without user evidence."""
        W.store_details(store_id)
        with W.A.db() as c: return [json.loads(r['payload']) for r in c.execute('SELECT payload FROM assets WHERE store_id=? ORDER BY asset_id',(store_id,))]

    return {fn.__name__:dspy.Tool(fn) for fn in (create_ticket,update_ticket,update_checklist,get_ticket,lookup_asset,lookup_store,list_store_assets)}


class Invocation(BaseModel):
    ticket_id: str | None = None
    version: int | None = None
    arguments: dict = Field(default_factory=dict)


def install(app,W):
    auth=[Depends(W.A.auth)]
    @app.get('/api/agent/tools',dependencies=auth)
    def tools():
        return [{'name':t.name,'description':t.desc,'parameters':{'type':'object','properties':t.args,'required':list(t.args)}} for t in registry(W).values()]

    @app.post('/api/agent/tools/{name}',dependencies=auth)
    def invoke(name:str,body:Invocation):
        with W.LOCK:
            ticket=W.load(body.ticket_id) if body.ticket_id else None
            if name in ('update_ticket','update_checklist'):
                if ticket is None or body.version is None: raise HTTPException(422,'Ticket ID and current version are required for updates.')
                W.check_version(ticket,body.version)
            tool=registry(W,ticket,persist=True).get(name)
            if not tool: raise HTTPException(404,'Unknown agent tool.')
            try: return tool(**body.arguments)
            except HTTPException: raise
            except (ValueError,TypeError): raise HTTPException(422,'Invalid tool arguments. Read /api/agent/tools for the schema.') from None
