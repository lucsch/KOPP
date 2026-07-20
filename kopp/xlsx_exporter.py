from openpyxl import Workbook


class XlsxExporter:
    """Export rows to an XLSX workbook."""

    @staticmethod
    def export(filename, headers, rows):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Records"

        worksheet.append(list(headers))
        for row in rows:
            worksheet.append(["" if value is None else value for value in row])

        workbook.save(filename)
