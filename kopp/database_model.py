#!/usr/bin/env/ python3

from peewee import *

# Create a "Proxy". This allows defining models first,
# and linking the database file later via parameters.
database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

# Definition of the 'errors' table
class Errors(BaseModel):
    id = IntegerField(primary_key=True)
    desc = CharField(null=True)  # Equivalent to TEXT / VARCHAR

    class Meta:
        table_name = 'errors'

# Definition of the 'records' table
class Records(BaseModel):
    record_id = AutoField()  # AutoField automatically handles the INTEGER PRIMARY KEY AUTOINCREMENT
    date = DateTimeField(null=True)  # Peewee will automatically convert Python datetime objects to TEXT for SQLite
    hr_base = IntegerField(null=True)
    hr_maj = IntegerField(null=True)
    annual = IntegerField(null=True)
    vac = IntegerField(null=True)
    # Definition of the foreign key to the Errors table
    error = ForeignKeyField(Errors, backref='records', column_name='error_id', field='id', null=True)
    comment = CharField(null=True)

    class Meta:
        table_name = 'records'