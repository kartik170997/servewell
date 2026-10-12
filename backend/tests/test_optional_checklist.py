from test_api import client,providers,main
from test_live_workflow import live,start,final,feedback

W=main.ticket_workflow


def toggle(client,t,enabled):
    r=client.put('/api/tickets/'+t['ticket_id']+'/information',json={'version':t['version'],'information':{},'checklist_optional':enabled})
    assert r.status_code==200,r.text
    return r.json()


def test_optional_mode_asks_once_then_handoff_with_less_than_15_minutes(client,live,monkeypatch):
    t=toggle(client,final(start(client)),True)
    t=final(feedback(client,t,minutes_spent=1))
    assert t['workflow']['pending']['kind']=='step'
    t=final(feedback(client,t,minutes_spent=1))
    assert t['workflow']['pending']['kind']=='information'
    assert t['checklist_optional'] is True
    def unexpected_model_extraction(*args,**kwargs): raise AssertionError('A blank optional answer needs no model call')
    monkeypatch.setattr(main.live_workflow,'capture_information',unexpected_model_extraction)
    t=final(feedback(client,t,outcome='answer',note='',minutes_spent=0))
    assert t['status']=='Escalated'
    assert t['workflow']['pending'] is None
    assert t['workflow']['optional_checklist_asked']
    assert t['workflow']['notification_draft']['sent'] is False
    assert not t['workflow']['missing_information']


def test_toggle_off_restores_required_fields_and_time_gate(client,live):
    t=toggle(client,final(start(client)),True)
    t=toggle(client,t,False)
    t=final(feedback(client,t,minutes_spent=1))
    t=final(feedback(client,t,minutes_spent=1))
    assert t['workflow']['pending']['kind']=='information'
    assert '15 minutes' in t['workflow']['pending']['message']
    assert not t['escalation_flag']


def test_enabling_while_already_asked_does_not_ask_again(client,live):
    t=final(start(client))
    t=final(feedback(client,t,minutes_spent=1))
    t=final(feedback(client,t,minutes_spent=1))
    assert t['workflow']['pending']['kind']=='information'
    t=toggle(client,t,True)
    t=final(feedback(client,t,outcome='answer',note='',minutes_spent=0))
    assert t['status']=='Escalated'


def test_store_id_is_still_required_and_skipped_steps_do_not_handoff(client,live):
    assert W.missing_info({'checklist_optional':True,'store_id':'UNSPECIFIED'})==['store ID']
    t=toggle(client,final(start(client)),True)
    t=final(feedback(client,t,outcome='skipped',note='Skipped',minutes_spent=0))
    t=final(feedback(client,t,minutes_spent=1))
    assert not t['escalation_flag']
    assert t['workflow']['pending']['kind']=='step'
