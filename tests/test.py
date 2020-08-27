"""Used to define test cases by creating new """
import unittest
from peewee import *

test_db = SqliteDatabase("test_db")


class BaseModel(Model):
    """Base model"""

    class Meta:
        database = test_db


class Cities(BaseModel):
    """
    City table Model
    """

    City_id = CharField(primary_key=True)
    city_name = CharField()


class Weather(BaseModel):
    """
    Weather table Model
    """

    city_id = ForeignKeyField(Cities, null=True)
    datetime = TextField()
    weather_state_name = CharField()
    temperature = CharField()


class TestCases(unittest.TestCase):
    """Test case writing"""

    def setUp(self):
        # test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()

        test_db.create_tables([Cities, Weather])

        self.city = Cities()
        self.weather = Weather()

    def tearDown(self):
        test_db.drop_tables([Cities, Weather])
        test_db.close()

    async def test_create(self):
        city_name = "Pune"
        get_data = get_city_name(city_name)
        query = Cities.get(Cities.city_name == city_name)
        self.assertEqual(query, None)
        city_data = []
        city_details = {
            "city_id": get_data[0]["woeid"],
            "city_name": get_data[0]["title"],
        }
        city_data.append(city_details)

        for city in city_data:
            query = Cities.create(
                City_id=city.get("city_id"), city_name=city.get("city_name")
            )

        self.assertEqual(query, 200)

    async def test_delete(self):
        city_id = "2295412"
        City_del = await self.Cities.select().where(Weather.city_id == city_id)
        if not City_del:
            self.assertEqual(weather_data_del, 404)

        query = await self.Cities.delete().where(Cities.city_id == city_id).execute()
        self.assertEqual(query, 200)

    async def test_get(self):
        query = await self.Cities.select().execute()

        self.assertEqual(query, 200)


def get_city_name(new_city):
    url = "https://www.metaweather.com/api/location/search/?query={}"

    r = requests.get(url.format(new_city)).json()

    return r
