from collections import OrderedDict


class MainListViewData:
    """Main records list column names and widths."""

    column_info = OrderedDict([
        ("Date", 150),
        ("HR", 70),
        ("A", 70),
        ("VAC", 70),
        ("Tags", 130),
        ("Comment", 200),
    ])


class MainListRows:
    def __init__(self):
        self.rows = []

    def append_item(self, values, data):
        self.rows.append(self._make_row(values, data))

    def delete_item(self, row):
        if not self._has_row(row):
            return False
        del self.rows[row]
        return True

    def delete_all_items(self):
        self.rows.clear()

    def get_value(self, row, column):
        try:
            if not self._has_row(row) or not self._has_column(column):
                return ""
            return self.rows[row]["values"][column]
        except Exception:
            return ""

    def set_value(self, value, row, column):
        if not self._has_row(row) or not self._has_column(column):
            return False
        self.rows[row]["values"][column] = value
        self.rows[row]["negative_columns"] = self._get_negative_columns(self.rows[row]["values"])
        return True

    def set_item_data(self, row, data):
        if not self._has_row(row):
            return False
        self.rows[row]["data"] = data
        return True

    def get_item_data(self, row):
        if not self._has_row(row):
            return None
        return self.rows[row]["data"]

    def has_negative_value(self, row, column):
        if not self._has_row(row):
            return False
        return self.rows[row]["negative_columns"].get(column, False)

    def _make_row(self, values, data):
        values = self._normalize_values(values)
        return {
            "values": values,
            "data": data,
            "negative_columns": self._get_negative_columns(values),
        }

    def _normalize_values(self, values):
        values = list(values)
        column_count = self.column_count()
        if len(values) < column_count:
            values += [""] * (column_count - len(values))
        return values[:column_count]

    def _get_negative_columns(self, values):
        return {
            column: values[column].startswith("-")
            for column in (1, 2, 3)
            if column < len(values)
        }

    def _has_row(self, row):
        return 0 <= row < len(self.rows)

    def _has_column(self, column):
        return 0 <= column < self.column_count()

    @staticmethod
    def column_count():
        return len(MainListViewData.column_info)
