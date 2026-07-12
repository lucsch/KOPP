#!/usr/bin/env/ python3

from peewee import Proxy, Model, AutoField, DateTimeField, IntegerField, CharField, ForeignKeyField, CompositeKey

# Create a "Proxy". This allows defining models first,
# and linking the database file later via parameters.
database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

# Table 'records'
class Records(BaseModel):
    record_id = AutoField()  # Handled as INTEGER PRIMARY KEY AUTOINCREMENT
    date = DateTimeField(null=True)
    hr_base = IntegerField(null=True)
    hr_maj = IntegerField(null=True)
    annual = IntegerField(null=True)
    vac = IntegerField(null=True)
    comment = CharField(null=True)

    class Meta:
        table_name = 'records'

# Table 'tags'
class Tags(BaseModel):
    id = AutoField()  # Handled as INTEGER PRIMARY KEY AUTOINCREMENT
    desc = CharField(null=True)

    class Meta:
        table_name = 'tags'

# Table 'tagsmix' (Junction table for Many-to-Many relationship)
class Tagsmix(BaseModel):
    record = ForeignKeyField(Records, backref='tags_mix', column_name='record_id', field='record_id')
    tag = ForeignKeyField(Tags, backref='records_mix', column_name='tag_id', field='id')

    class Meta:
        table_name = 'tagsmix'
        # Creates a composite primary key to avoid duplicate record-tag pairs
        primary_key = CompositeKey('record', 'tag')