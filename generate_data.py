import requests

def get_city_name(new_city):
    """
    :description: Used to city records.
    :param new_city:
    :return:
    """
    url = 'https://www.metaweather.com/api/location/search/?query={}'

    res = requests.get(url.format(new_city)).json()
    city_details = {
        "city_id": res[0]["woeid"],
        "city_name": res[0]["title"],
    }

    return city_details


def get_city_data(city_id):
    """
    :description: Used to city's weather records.
    :param new_city:
    :return:
    """
    url = 'https://www.metaweather.com/api/location/{}/'
    # print("url is======================", url)
    res = requests.get(url.format(city_id)).json()

    return res