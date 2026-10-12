from test_api import client, providers, main
from test_live_workflow import live, start, final

L=main.live_workflow
W=main.ticket_workflow


def test_screenshot_details_are_saved_with_na_count(client,live):
    t=final(start(client))
    L.capture_information(t,'frequency - one or 2 times a day\nnumber of afftected devices - 1\nafftected users - NA\ncontrtact metod - Phone\nCustomer name - Kartik',decision={})
    assert t['submitted_by']=='Kartik'
    assert t['escalation_info']['frequency']=='one or 2 times a day'
    assert t['escalation_info']['affected_devices']==1
    assert t['escalation_info']['affected_users']=='N/A'
    assert t['escalation_info']['preferred_contact']=='Phone'
    missing=W.missing_info(t)
    assert not set(missing)&{'issue frequency','number of affected devices','number of affected users','preferred contact method','verified customer name'}


def test_invalid_count_does_not_discard_other_fields(client,live):
    t=final(start(client))
    L.capture_information(t,'frequency - daily\naffected users - -2\nCustomer name - Kartik',decision={})
    assert t['submitted_by']=='Kartik'
    assert t['escalation_info']['frequency']=='daily'
    assert not t['escalation_info'].get('affected_users')
    assert any('affected_users' in x['note'] for x in t['ticket_history'] if x['actor']=='L1 Agent')


def test_earlier_rejected_answer_recovered_without_overwriting_saved_values(client,live):
    t=final(start(client))
    t['ticket_history'].append({'actor':'User','note':'Feedback: answer. Details:\nfrequency - daily\nCustomer name - Kartik\nafftected users - NA'})
    t['escalation_info']['frequency']='hourly'
    L.capture_information(t,'Continue',decision={})
    assert t['submitted_by']=='Kartik'
    assert t['escalation_info']['frequency']=='hourly'
    assert t['escalation_info']['affected_users']=='N/A'
