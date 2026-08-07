from kopp.infodataimporter import InfoDataImporter

def test_infodataimporter_basic():
    importer = InfoDataImporter()
    assert not importer.process("")
    data = importer.get_processed_data()
    assert data.title == ""
    assert data.hr_done_hours == 0
    assert data.hr_done_minutes == 0
    assert data.hr_increased_hours == 0
    assert data.hr_increased_minutes == 0
    assert data.hr_total_hours == 0
    assert data.hr_total_minutes == 0
    assert data.a_hours == 0
    assert data.a_minutes == 0
    assert data.piquet_hours == 0
    assert data.piquet_minutes == 0
    assert data.vac_hours == 0
    assert data.vac_minutes == 0

