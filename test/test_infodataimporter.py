from kopp.infodataimporter import InfoDataImporter, InfoLineType

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

    assert importer._get_minutes_from_line("112h10m") == 6730
    assert importer._get_minutes_from_line("0h00m") == 0
    assert importer._get_minutes_from_line("24h45m") == 1485


def test_process_line_hours_with_days():
    importer = InfoDataImporter()

    assert importer._get_minutes_from_line("13,50j") == 6480
    assert importer._get_minutes_from_line("0,0j") == 0
    assert importer._get_minutes_from_line("0,50j") == 240


def test_get_type_of_line():
    importer = InfoDataImporter()

    assert importer._get_type_of_line("Annualisation") == InfoLineType.ANNUALISATION
    assert importer._get_type_of_line("Solde Vacances") == InfoLineType.SOLDE_VACANCES
    assert importer._get_type_of_line("Solde HS") == InfoLineType.SOLDE_HS
    assert importer._get_type_of_line("Solde HS A-1") == InfoLineType.SOLDE_HS_A_1
    assert importer._get_type_of_line("Solde piquet") == InfoLineType.SOLDE_PIQUET
    assert importer._get_type_of_line("Solde piquet A-1") == InfoLineType.SOLDE_PIQUET_A_1
    assert importer._get_type_of_line("Unknown") == InfoLineType.UNKNOWN

def test_process():
    importer = InfoDataImporter()
    assert not importer.process("")

    str = """
Annualisation
123h30m
 
Débit / crédit
0h00m
 
Solde Vacances
13,00j
 
HS effectives
112h10m
 
majoration 25 %
24h45m
 
majoration 50 %
0h00m
 
majoration 100 %
12h30m
 
HS majorées
149h25m
 
Solde HS
149h25m
 
Solde HS A-1
2h41m
 
Solde HS 2009
0h00m
 
Piquet brut
250h00m
 
Piquet net
150h30m
 
Compensation piquet
22h32m
 
Inter. sur piquet en service
0h00m
 
Inter. sur piquet hors service
0h00m
 
Maj intervention piquet 25 %
0h00m
 
Maj intervention piquet 100 %
0h00m
 
Intervention piquet majorée
0h00m
 
Solde piquet
22h32m
 
Solde piquet A-1
0h00m
 
Solde HC
0h00m
 
Solde HC A-1
0h00m
 
Débours
80h15m
 
Heures de nuit
41h30m
    """
    assert importer.process(str)
    data = importer.get_processed_data()
    assert data.title == ""
    assert data.hr_total_hours == 152
    assert data.hr_total_minutes == 6
    assert data.piquet_hours == 22
    assert data.piquet_minutes == 32
    assert data.vac_hours == 104
    assert data.vac_minutes == 0
    assert data.a_hours == 123
    assert data.a_minutes == 30
