from aiohttp import web
from views.operations import CityViews, WeatherViews

URL = '/all_data'
def get_app():
    """
    @description - Used to create database session and calls HTTP methods
    @returns - returns web app
    """

    app = web.Application(debug=True)
    app.router.add_route("*",  "/", CityViews, name="city")
    app.router.add_route("*", "/{id}", CityViews, name="city_id")
    app.router.add_route("*", URL + "/weather", WeatherViews, name="weather")

    return app

if __name__ == '__main__':
    web.run_app(get_app())