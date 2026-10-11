import json
import pytest
from test_api import client, main
import import_directory as importer


def test_import_is_complete_idempotent_and_transactional(client,tmp_path,monkeypatch):
    monkeypatch.setattr(importer,'main',main)
    folder=tmp_path/'csv';folder.mkdir()
    stores=folder/'stores.csv';assets=folder/'assets.csv'
    stores.write_text('store_id,store_name,city,support_phone\nS1,Store One,Mumbai,+91-123\n')
    assets.write_text('asset_id,store_id,asset_type,system_version,serial_number\nA1,S1,Printer,v1,SERIAL1\n')
    assert importer.import_directory(folder)=={'stores':1,'assets':1}
    importer.import_directory(folder)
    with main.db() as c:
        assert c.execute('select count(*) from stores').fetchone()[0]==1
        assert c.execute('select count(*) from assets').fetchone()[0]==1
    data=client.get('/api/asset-context/A1').json()
    assert data['asset']['serial_number']=='SERIAL1' and data['store']['city']=='Mumbai'
    stores.write_text('store_id,store_name\nS2,Store Two\n')
    assets.write_text('asset_id,store_id\nA2,MISSING\n')
    with pytest.raises(ValueError,match='unknown stores'): importer.import_directory(folder)
    with main.db() as c: assert not c.execute("select 1 from stores where store_id='S2'").fetchone()
    assets.write_text('asset_id,store_id\nA2,S2\nA2,S2\n')
    with pytest.raises(ValueError,match='duplicate'): importer.import_directory(folder)
