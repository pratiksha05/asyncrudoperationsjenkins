"""Database defined here."""
from peewee import SqliteDatabase, Model, CharField, TextField, ForeignKeyField


sq_db = SqliteDatabase("my_db")


class BaseModel(Model):
    """Base model"""

    class Meta:
        database = sq_db


class Cities(BaseModel):
    """
    City table Model
    """

    city_id = CharField(primary_key=True)
    city_name = CharField()


class Weather(BaseModel):
    """
    Weather table model
    """

    city_id = ForeignKeyField(Cities, null=True)
    city_name = CharField()
    datetime = TextField()
    weather = CharField()
    temperature = CharField()


sq_db.connect()
sq_db.create_tables([Cities, Weather])
