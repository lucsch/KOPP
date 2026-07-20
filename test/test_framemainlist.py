from kopp.framemainlist import FrameMainListModel


def test_model_normalizes_short_rows_and_ignores_out_of_bounds_cells():
    model = FrameMainListModel()
    model.append_item(["date"], 1)

    assert model.GetValueByRow(0, 0) == "date"
    assert model.GetValueByRow(0, 5) == ""
    assert model.GetValueByRow(0, 6) == ""
    assert model.GetValueByRow(1, 0) == ""


def test_model_rejects_out_of_bounds_updates():
    model = FrameMainListModel()
    model.append_item(["date"], 1)

    assert model.SetValueByRow("value", 0, 6) is False
    assert model.SetValueByRow("value", 1, 0) is False
