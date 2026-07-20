from dataclasses import dataclass
from datetime import datetime

from peewee import fn

from kopp.database_model import Records


@dataclass(frozen=True)
class RecordTotals:
    hr_base: int = 0
    hr_maj: int = 0
    annual: int = 0
    vac: int = 0


@dataclass(frozen=True)
class RecordCumulativeTotals:
    date: datetime
    hr_total: int = 0
    annual: int = 0
    vac: int = 0


class RecordTotalsCalculator:
    """Compute aggregate minute totals for records."""

    @classmethod
    def all(cls) -> RecordTotals:
        return cls.until_record_id(None)

    @classmethod
    def until_record_id(cls, record_id: int | None) -> RecordTotals:
        query = Records.select(
            fn.COALESCE(fn.SUM(Records.hr_base), 0).alias("hr_base"),
            fn.COALESCE(fn.SUM(Records.hr_maj), 0).alias("hr_maj"),
            fn.COALESCE(fn.SUM(Records.annual), 0).alias("annual"),
            fn.COALESCE(fn.SUM(Records.vac), 0).alias("vac"),
        )

        if record_id is not None:
            if not isinstance(record_id, int):
                raise TypeError("record_id must be an integer or None")
            record = Records.select(Records.record_id, Records.date).where(Records.record_id == record_id).first()
            if record is None:
                return RecordTotals()

            if record.date is None:
                query = query.where(
                    Records.date.is_null(True)
                    & (Records.record_id <= record.record_id)
                )
            else:
                query = query.where(
                    Records.date.is_null(True)
                    | (Records.date < record.date)
                    | ((Records.date == record.date) & (Records.record_id <= record.record_id))
                )

        row = query.dicts().get()
        return RecordTotals(
            hr_base=row["hr_base"],
            hr_maj=row["hr_maj"],
            annual=row["annual"],
            vac=row["vac"],
        )


class RecordCumulativeTotalsCalculator:
    """Compute cumulative minute totals grouped by record date."""

    @classmethod
    def all(cls) -> list[RecordCumulativeTotals]:
        totals = cls._undated_totals()
        cumulative_hr_total = totals.hr_base + totals.hr_maj
        cumulative_annual = totals.annual
        cumulative_vac = totals.vac
        cumulative_totals = []

        for row in cls._dated_totals_query():
            cumulative_hr_total += row["hr_base"] + row["hr_maj"]
            cumulative_annual += row["annual"]
            cumulative_vac += row["vac"]
            cumulative_totals.append(
                RecordCumulativeTotals(
                    date=row["date"],
                    hr_total=cumulative_hr_total,
                    annual=cumulative_annual,
                    vac=cumulative_vac,
                )
            )

        return cumulative_totals

    @classmethod
    def _undated_totals(cls) -> RecordTotals:
        row = (
            Records.select(
                fn.COALESCE(fn.SUM(Records.hr_base), 0).alias("hr_base"),
                fn.COALESCE(fn.SUM(Records.hr_maj), 0).alias("hr_maj"),
                fn.COALESCE(fn.SUM(Records.annual), 0).alias("annual"),
                fn.COALESCE(fn.SUM(Records.vac), 0).alias("vac"),
            )
            .where(Records.date.is_null(True))
            .dicts()
            .get()
        )
        return RecordTotals(
            hr_base=row["hr_base"],
            hr_maj=row["hr_maj"],
            annual=row["annual"],
            vac=row["vac"],
        )

    @classmethod
    def _dated_totals_query(cls):
        return (
            Records.select(
                Records.date.alias("date"),
                fn.COALESCE(fn.SUM(Records.hr_base), 0).alias("hr_base"),
                fn.COALESCE(fn.SUM(Records.hr_maj), 0).alias("hr_maj"),
                fn.COALESCE(fn.SUM(Records.annual), 0).alias("annual"),
                fn.COALESCE(fn.SUM(Records.vac), 0).alias("vac"),
            )
            .where(Records.date.is_null(False))
            .group_by(Records.date)
            .order_by(Records.date)
            .dicts()
        )
