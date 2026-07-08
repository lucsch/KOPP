#!/usr/bin/env/ python3

from kopp.database_model import database_proxy, Tags, Records, Tagsmix
from peewee import *
import os
import sqlite3
import wx

class Database:
    def __init__(self, database_filename:str):
        self.database_filename = database_filename
        db = SqliteDatabase(self.database_filename, pragmas={
            # 'journal_mode': 'wal',  # Allow readers while writer active. (generate multiple wal and shm files)
            'cache_size': -64000,  # 64 MB page cache.
            'foreign_keys': 1,  # Enforce FK constraints.
        })
        database_proxy.initialize(db)

        db.connect()
        db.create_tables([Tags, Records, Tagsmix])
        self.db = db

    def close(self):
        self.db.close()


class ProjectDatabase:
    def __init__(self):
        self.database = None
        self.database_filename = None

    def __del__(self):
        self.close_project()

    def new_project(self):
        """Create a new project database in memory"""
        self.close_project()
        self.database = Database(':memory:')
        self.database_filename = None

    def open_project(self, database_filename:str) -> bool:
        if not database_filename:
            return False

        if not os.path.exists(database_filename):
            return False

        self.close_project()
        self.database = Database(database_filename)
        self.database_filename = database_filename
        return True

    def save_project(self, database_filename:str) -> bool:
        """Open a direct sqlite connection to the database file and copy the database to the file"""
        if not self.database:
            wx.LogError("No database to save")
            return False

        # do the backup
        conn_file = sqlite3.connect(database_filename)
        conn_memoire = self.database.db.connection()
        with conn_file:
            conn_memoire.backup(conn_file)
        conn_file.close()

        # open the backup
        self.open_project(database_filename)
        return True

    def close_project(self):
        if self.database:
            self.database.close()
        self.database = None
        self.database_filename = None