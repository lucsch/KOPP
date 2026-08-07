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


def test_process_line_hours_with_hours_and_minutes():
    importer = InfoDataImporter()

    assert importer._process_line_hours("112h10m") == 6730
    assert importer._process_line_hours("0h00m") == 0
    assert importer._process_line_hours("24h45m") == 1485


def test_process_line_hours_with_days():
    importer = InfoDataImporter()

    assert importer._process_line_hours("13,50j") == 6480
    assert importer._process_line_hours("0,0j") == 0
    assert importer._process_line_hours("0,50j") == 240
