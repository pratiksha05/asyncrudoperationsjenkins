"""Used to perform Crud operations"""
import logging
from aiohttp import web
from model.db import Cities, Weather
from generate_data import get_city_name, get_city_data
from logger import ContextualLogger

logger = ContextualLogger(logging.getLogger("Weather"))


class CityViews(web.View):
    """Used to define HTTP methods"""

    async def post(self):
        """
        @description - Used to insert Weather records.
        @param - self: post request with data to insert.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        try:
            data = await self.request.json()
            new_city = data["city"]
            new_city_id = data["id"]
            city_data = get_city_name(new_city)
            city = Cities.filter(Cities.city_id == new_city_id).first()
            weather = Weather.filter(Weather.city_id == new_city_id).first()
            if city and weather:
                response_obj = {"message": "Weather data already exist"}
                return web.Response(text=str(response_obj), status=404)
            else:
                Cities.create(
                    city_id=city_data.get("city_id"),
                    city_name=city_data.get("city_name"),
                )
                city_id = city_data.get("city_id")
                api_data_details = get_city_data(city_id)
                api_data = api_data_details["consolidated_weather"]
                city_name = city_data.get("city_name")
                for data in api_data:
                    api_date = data["applicable_date"]
                    weather_name = data["weather_state_name"]
                    temperature = data["the_temp"]
                    Weather.create(
                        city_id=city_id,
                        city_name=city_name,
                        datetime=api_date,
                        weather=weather_name,
                        temperature=temperature,
                    )
                response_obj = {"message": "Weather data added"}
                return web.Response(text=str(response_obj), status=200)

        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
            response_obj = {"message": str(ex)}
            return web.Response(text=str(response_obj), status=500)

    async def put(self):
        """
        @description - Used to update Weather record.
        @param - self: put request with id to update record and data to update.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        try:
            data = await self.request.json()
            city_name = data["city_name"]
            city_id = data["city_id"]
            weather_obj = Weather.filter(Weather.city_name == city_name).first()
            if not weather_obj:
                response_obj = {"status": "failed"}
                logger.error("No data found!!!")
                return web.Response(text=str(response_obj), status=404)

            weather_data = get_city_data(city_id)
            weathe_data_dict = weather_data["consolidated_weather"]
            all_dates = [data.get("applicable_date") for data in weathe_data_dict]
            for date in all_dates:
                is_date_present = Weather.get(Weather.datetime == date)
                for weather_data in weathe_data_dict:
                    if is_date_present:
                        Weather.update(
                            city_id=city_id,
                            city_name=city_name,
                            datetime=weather_data["applicable_date"],
                            weather=weather_data["weather_state_name"],
                            temperature=weather_data["the_temp"],
                        )
                        logger.info("Weather data  updated!!!")

                    else:
                        Weather.create(
                            city_id=city_id,
                            city_name=city_name,
                            datetime=weather_data["applicable_date"],
                            weather=weather_data["weather_state_name"],
                            temperature=weather_data["the_temp"],
                        )

                        logger.info("Data inserted successfully!!!")
            response_obj = {"message": "successful"}
            return web.Response(text=str(response_obj), status=204)
        except Exception as ex:
            response_obj = {"status": "failed"}
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)

    async def get(self):
        """@param - self: request with URL:'/'
           @returns - response with success status.
        """
        try:
            city_id = self.request.match_info["id"]
            if city_id:
                weather_data = Weather.select().where(Weather.city_id == city_id)
                weather_details = []
                for weather in weather_data:
                    weather_dict = {
                        "city_id": weather.city_id,
                        "city_name": weather.city_name,
                        "date": weather.datetime,
                        "weather_state_name": weather.weather,
                        "temperature": weather.temperature,
                    }
                    weather_details.append(weather_dict)
                response_obj = {"message": weather_details, "status": 200}
                return web.Response(text=str(response_obj))
        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=error_message, status=500)

    async def delete(self):
        """
        @description - Used to delete  record
        @param - self: delete request with id to delete record.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        try:
            data = await self.request.json()
            city_name = data.get("city_name")
            weather_data_del = Weather.select().where(Weather.city_name == city_name)
            if not weather_data_del:
                response_obj = {"status": "failed", "reason": "City not Present"}
                return web.Response(text=str(response_obj), status=500)
            try:

                Weather.delete().where(Weather.city_name == city_name).execute()
                logger.info("System deleted successfully!!!")
                response_obj = {"status": "Record Deleted successfully"}
                return web.Response(text=str(response_obj), status=200)
            except Exception as ex:
                response_obj = {"status": "failed", "reason": str(ex)}
                error_message = str(ex)
                logger.error(error_message)
                return web.Response(text=str(response_obj), status=500)
        except Exception as ex:
            response_obj = {"status": "failed", "reason": str(ex)}
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)


class WeatherViews(web.View):
    """Used to define HTTP methods"""

    async def get(self):
        """
        @description - Used to get Get all the weather records.
        @param - self: Get request.
        @returns - response with status 200 in case of success and 404 in case of exception.
        """
        try:
            query = Weather.select().execute()
            weather_details = []
            for data in query:
                weather_dict = {
                    "city_id": data.city_id,
                    "city_name": data.city_name,
                    "date": data.datetime,
                    "weather": data.weather,
                    "temperature": data.temperature,
                }
                weather_details.append(weather_dict)
            return web.Response(body=str(weather_details), status=200)
        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(error_message), status=404)
