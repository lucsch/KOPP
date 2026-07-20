from datetime import datetime

import pytest

from kopp.database import Database
from kopp.database_model import Records
from kopp.record_totals import (
    RecordCumulativeTotals,
    RecordCumulativeTotalsCalculator,
    RecordTotals,
    RecordTotalsCalculator,
)


@pytest.fixture
def database():
    db = Database(":memory:")
    yield db
    db.close()


def create_record(hr_base=None, hr_maj=None, annual=None, vac=None, date=None):
    return Records.create(
        date=date,
        hr_base=hr_base,
        hr_maj=hr_maj,
        annual=annual,
        vac=vac,
    )


def test_all_returns_zero_totals_for_empty_database(database):
    assert RecordTotalsCalculator.all() == RecordTotals()


def test_all_sums_all_record_values(database):
    create_record(hr_base=60, hr_maj=30, annual=10, vac=5)
    create_record(hr_base=15, hr_maj=-10, annual=20, vac=25)
    create_record(hr_base=None, hr_maj=None, annual=None, vac=None)

    assert RecordTotalsCalculator.all() == RecordTotals(
        hr_base=75,
        hr_maj=20,
        annual=30,
        vac=30,
    )


def test_until_record_id_sums_values_up_to_included_id(database):
    first = create_record(hr_base=60, hr_maj=30, annual=10, vac=5)
    second = create_record(hr_base=15, hr_maj=-10, annual=20, vac=25)
    create_record(hr_base=100, hr_maj=100, annual=100, vac=100)

    assert RecordTotalsCalculator.until_record_id(first.record_id) == RecordTotals(
        hr_base=60,
        hr_maj=30,
        annual=10,
        vac=5,
    )
    assert RecordTotalsCalculator.until_record_id(second.record_id) == RecordTotals(
        hr_base=75,
        hr_maj=20,
        annual=30,
        vac=30,
    )


def test_until_record_id_uses_display_order_by_date_then_id(database):
    later = create_record(hr_base=100, date=datetime(2026, 1, 3))
    first = create_record(hr_base=10, date=datetime(2026, 1, 1))
    second = create_record(hr_base=20, date=datetime(2026, 1, 2))
    same_date = create_record(hr_base=5, date=datetime(2026, 1, 2))

    assert later.record_id < first.record_id
    assert RecordTotalsCalculator.until_record_id(second.record_id) == RecordTotals(hr_base=30)
    assert RecordTotalsCalculator.until_record_id(same_date.record_id) == RecordTotals(hr_base=35)


def test_until_record_id_keeps_null_dates_first_like_display_order(database):
    null_date = create_record(hr_base=10)
    dated = create_record(hr_base=20, date=datetime(2026, 1, 1))

    assert RecordTotalsCalculator.until_record_id(null_date.record_id) == RecordTotals(hr_base=10)
    assert RecordTotalsCalculator.until_record_id(dated.record_id) == RecordTotals(hr_base=30)


def test_until_record_id_returns_zero_when_no_record_matches(database):
    create_record(hr_base=60, hr_maj=30, annual=10, vac=5)

    assert RecordTotalsCalculator.until_record_id(0) == RecordTotals()


def test_until_record_id_rejects_non_integer_id(database):
    with pytest.raises(TypeError):
        RecordTotalsCalculator.until_record_id("1")


def test_cumulative_totals_returns_empty_list_for_empty_database(database):
    assert RecordCumulativeTotalsCalculator.all() == []


def test_cumulative_totals_groups_by_date_and_accumulates_values(database):
    first_date = datetime(2026, 1, 1)
    second_date = datetime(2026, 1, 2)

    create_record(hr_base=60, hr_maj=30, annual=10, vac=5, date=first_date)
    create_record(hr_base=15, hr_maj=-10, annual=20, vac=25, date=second_date)
    create_record(hr_base=None, hr_maj=None, annual=None, vac=None, date=second_date)

    assert RecordCumulativeTotalsCalculator.all() == [
        RecordCumulativeTotals(date=first_date, hr_total=90, annual=10, vac=5),
        RecordCumulativeTotals(date=second_date, hr_total=95, annual=30, vac=30),
    ]


def test_cumulative_totals_combines_records_with_the_same_date(database):
    record_date = datetime(2026, 1, 1)

    create_record(hr_base=60, hr_maj=30, annual=10, vac=5, date=record_date)
    create_record(hr_base=15, hr_maj=-10, annual=20, vac=25, date=record_date)

    assert RecordCumulativeTotalsCalculator.all() == [
        RecordCumulativeTotals(date=record_date, hr_total=95, annual=30, vac=30),
    ]


def test_cumulative_totals_uses_chronological_order(database):
    later = datetime(2026, 1, 3)
    first = datetime(2026, 1, 1)
    second = datetime(2026, 1, 2)

    create_record(hr_base=100, date=later)
    create_record(hr_base=10, date=first)
    create_record(hr_base=20, date=second)

    assert RecordCumulativeTotalsCalculator.all() == [
        RecordCumulativeTotals(date=first, hr_total=10),
        RecordCumulativeTotals(date=second, hr_total=30),
        RecordCumulativeTotals(date=later, hr_total=130),
    ]


def test_cumulative_totals_uses_undated_records_as_initial_balance(database):
    create_record(hr_base=60, hr_maj=30, annual=10, vac=5)
    record_date = datetime(2026, 1, 1)
    create_record(hr_base=15, hr_maj=-10, annual=20, vac=25, date=record_date)

    assert RecordCumulativeTotalsCalculator.all() == [
        RecordCumulativeTotals(date=record_date, hr_total=95, annual=30, vac=30),
    ]
