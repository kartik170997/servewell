import pytest
from test_api import client, main
from test_tickets import ticket


def test_tools_schema_and_auth(client):
    r=client.get('/api/agent/tools');assert r.status_code==200
    assert {'create_ticket','update_ticket','update_checklist','get_ticket','lookup_store','lookup_asset','list_store_assets'}=={t['name'] for t in r.json()}
    assert client.get('/api/agent/tools',headers={'Authorization':'Bearer wrong'}).status_code==401


def test_tool_updates_validate_versions_and_relationships(client):
    t=ticket(client)
    url='/api/agent/tools/update_checklist'
    body={'ticket_id':t['ticket_id'],'version':t['version'],'arguments':{'information':{'store_id':t['store_id'],'contact_phone':'12345'}}}
    assert client.post(url,json=body).status_code==200
    t2=client.get('/api/tickets/'+t['ticket_id']).json()
    assert t2['contact_phone']=='12345' and t2['escalation_info']['store_id']==t['store_id']
    assert client.post(url,json=body).status_code==409
    assert client.post(url,json={**body,'version':t2['version'],'arguments':{'information':{'store_id':'OTHER'}}}).status_code==422
    assert client.post('/api/agent/tools/update_ticket',json={**body,'version':t2['version'],'arguments':{'fields':{'status':'Resolved'}}}).status_code==422
    assert client.get('/api/tickets/'+t['ticket_id']).json()['status']=='Open'
    assert any(h['actor']=='Agent tool' for h in t2['ticket_history'])


def test_create_tool_uses_store_directory_and_rejects_duplicate(client):
    client.put('/api/ticket-directory/stores',json={'store_id':'SW-1234','store_name':'Verified store','city':'Pune'})
    body={'ticket_data':{'ticket_id':'TOOL-1','store_id':'SW-1234','store_name':'Ignore this','submitted_by':'Operator','date_opened':'2026-10-11T12:00:00+05:30','subject':'Network issue'}}
    r=client.post('/api/agent/tools/create_ticket',json={'arguments':body})
    assert r.status_code==200,r.text
    assert r.json()['store_name']=='Verified store'
    assert r.json()['escalation_info']['store_id']=='SW-1234'
    assert client.post('/api/agent/tools/create_ticket',json={'arguments':body}).status_code==409
    assert client.post('/api/agent/tools/lookup_store',json={'arguments':{'store_id':'SW-1234'}}).json()['city']=='Pune'
