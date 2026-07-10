from dataclasses import dataclass

from peewee import fn

from kopp.database_model import Records


@dataclass(frozen=True)
class RecordTotals:
    hr_base: int = 0
    hr_maj: int = 0
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
