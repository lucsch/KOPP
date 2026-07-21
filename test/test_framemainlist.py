from kopp.framemainlist_rows import MainListRows


def test_model_normalizes_short_rows_and_ignores_out_of_bounds_cells():
    model = MainListRows()
    model.append_item(["date"], 1)

    assert model.get_value(0, 0) == "date"
    assert model.get_value(0, 5) == ""
    assert model.get_value(0, 6) == ""
    assert model.get_value(1, 0) == ""


def test_model_rejects_out_of_bounds_updates():
    model = MainListRows()
    model.append_item(["date"], 1)

    assert model.set_value("value", 0, 6) is False
    assert model.set_value("value", 1, 0) is False
