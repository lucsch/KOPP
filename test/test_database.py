import sqlite3

from kopp.database import Database
from kopp.database_model import Records


def test_database_migrates_legacy_records_without_piquet(tmp_path):
    filename = tmp_path / "legacy.kdb"
    connection = sqlite3.connect(filename)
    connection.execute(
        """
        CREATE TABLE records (
            record_id INTEGER NOT NULL PRIMARY KEY,
            date DATETIME,
            hr_base INTEGER,
            hr_maj INTEGER,
            annual INTEGER,
            vac INTEGER,
            comment VARCHAR(255)
        )
        """
    )
    connection.execute(
        """
        INSERT INTO records
            (record_id, date, hr_base, hr_maj, annual, vac, comment)
        VALUES
            (1, '2026-01-01 00:00:00', 60, 30, 10, 5, 'legacy')
        """
    )
    connection.execute(
        """
        CREATE TABLE tags (
            id INTEGER NOT NULL PRIMARY KEY,
            desc VARCHAR(255)
        )
        """
    )
    connection.execute("INSERT INTO tags (id, desc) VALUES (1, 'tag')")
    connection.execute(
        """
        CREATE TABLE tagsmix (
            record_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (record_id, tag_id),
            FOREIGN KEY (record_id) REFERENCES records (record_id),
            FOREIGN KEY (tag_id) REFERENCES tags (id)
        )
        """
    )
    connection.execute("INSERT INTO tagsmix (record_id, tag_id) VALUES (1, 1)")
    connection.commit()
    connection.close()

    database = Database(filename)
    try:
        columns = [
            row[1]
            for row in database.db.execute_sql("PRAGMA table_info(records)").fetchall()
        ]
        record = Records.get_by_id(1)
        foreign_key_errors = database.db.execute_sql("PRAGMA foreign_key_check").fetchall()
        tagsmix_rows = database.db.execute_sql("SELECT record_id, tag_id FROM tagsmix").fetchall()

        assert columns == [
            "record_id",
            "date",
            "hr_base",
            "hr_maj",
            "annual",
            "piquet",
            "vac",
            "comment",
        ]
        assert record.piquet is None
        assert record.vac == 5
        assert record.comment == "legacy"
        assert foreign_key_errors == []
        assert tagsmix_rows == [(1, 1)]
    finally:
        database.close()
