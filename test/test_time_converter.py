import pytest

from kopp.timeconverter import TimeConverter


@pytest.mark.parametrize(
    ("hours", "minutes", "expected"),
    [
        (0, 0, 0),
        (0, 45, 45),
        (1, 0, 60),
        (1, -30, 30),
        (2, 30, 150),
        (-2, -30, -150),
        (100, 59, 6059),
    ],
)
def test_to_total_minutes(hours, minutes, expected):
    assert TimeConverter.to_total_minutes(hours, minutes) == expected


@pytest.mark.parametrize(
    ("total_minutes", "expected"),
    [
        (0, (0, 0)),
        (45, (0, 45)),
        (60, (1, 0)),
        (150, (2, 30)),
        (-30, (0, -30)),
        (-150, (-2, -30)),
        (6059, (100, 59)),
    ],
)
def test_from_total_minutes(total_minutes, expected):
    assert TimeConverter.from_total_minutes(total_minutes) == expected


@pytest.mark.parametrize(
    ("hours", "minutes"),
    [
        (0, 60),
        (0, -60),
    ],
)
def test_to_total_minutes_rejects_invalid_values(hours, minutes):
    with pytest.raises(ValueError):
        TimeConverter.to_total_minutes(hours, minutes)


@pytest.mark.parametrize(
    ("hours", "minutes"),
    [
        (1.5, 0),
        (1, "30"),
    ],
)
def test_to_total_minutes_rejects_non_integers(hours, minutes):
    with pytest.raises(TypeError):
        TimeConverter.to_total_minutes(hours, minutes)

@pytest.mark.parametrize("total_minutes", [1.5, "90"])
def test_from_total_minutes_rejects_non_integer(total_minutes):
    with pytest.raises(TypeError):
        TimeConverter.from_total_minutes(total_minutes)
