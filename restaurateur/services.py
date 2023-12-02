import requests
from geopy import distance

from star_burger.settings import YANDEX_API_GEOCODER


def fetch_coordinates(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": YANDEX_API_GEOCODER,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(restaurant, restaurant_address, order_address):
    try:
        restaurant_coords = fetch_coordinates(restaurant_address)
        order_coords = fetch_coordinates(order_address)
    except requests.exceptions:
        return 'Ошибка определения координат'
    total_distance = round(distance.distance(restaurant_coords, order_coords).km, 3)
    return f'{restaurant} - {total_distance} км'
