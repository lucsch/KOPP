from openpyxl import Workbook


class XlsxExporter:
    """Export records to an XLSX workbook."""

    headers = ["Day", "Date", "HR", "Annual", "VAC", "Tags", "Comment"]
    date_format = "dd.mm.yy"
    duration_format = "[h]:mm;-[h]:mm;0:00"

    @staticmethod
    def export(filename, rows):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Records"

        worksheet.append(XlsxExporter.headers)
        for row in rows:
            worksheet.append(
                [
                    row["day"],
                    row["date"],
                    XlsxExporter._minutes_to_excel_duration(row["hr"]),
                    XlsxExporter._minutes_to_excel_duration(row["annual"]),
                    XlsxExporter._minutes_to_excel_duration(row["vac"]),
                    row["tags"],
                    row["comment"],
                ]
            )

        for cell in worksheet["B"][1:]:
            cell.number_format = XlsxExporter.date_format

        for column in ("C", "D", "E"):
            for cell in worksheet[column][1:]:
                cell.number_format = XlsxExporter.duration_format

        workbook.save(filename)

    @staticmethod
    def _minutes_to_excel_duration(minutes):
        return (minutes or 0) / 24 / 60
