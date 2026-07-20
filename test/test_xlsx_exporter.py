from openpyxl import load_workbook

from kopp.xlsx_exporter import XlsxExporter


def test_export_writes_headers_and_rows_to_xlsx(tmp_path):
    filename = tmp_path / "records.xlsx"

    XlsxExporter.export(
        filename,
        ["Date", "HR", "A", "VAC", "Tags", "Comment"],
        [
            ["lundi 01.01.26", "1:30", "", "-2:00", "tag", "comment"],
            ["mardi 02.01.26", "2:00", "0:30", "", "", ""],
        ],
    )

    workbook = load_workbook(filename)
    worksheet = workbook["Records"]

    assert list(worksheet.iter_rows(values_only=True)) == [
        ("Date", "HR", "A", "VAC", "Tags", "Comment"),
        ("lundi 01.01.26", "1:30", None, "-2:00", "tag", "comment"),
        ("mardi 02.01.26", "2:00", "0:30", None, None, None),
    ]
