# flake8: noqa
from datetime import datetime

import requests
from django.core.cache import cache

from to_do_list.models import ListTasks


def sidebar_stuff(request):
    if request.user.is_authenticated:
        lists_tasks = ListTasks.objects.all()
        lists_tasks_menu = lists_tasks.filter(owner=request.user)
        lists_tasks_member_menu = []
        for list in lists_tasks:
            for member in list.members.all():
                if member == request.user:
                    lists_tasks_member_menu.append(list)
    else:
        lists_tasks_menu = None
        lists_tasks_member_menu = None

    return {
        'lists_tasks_menu': lists_tasks_menu,
        'lists_tasks_member_menu': lists_tasks_member_menu
    }


def weather(request):
    city_name = "Pelotas"
    cache_key = f'weather_{city_name}'

    if cache.get(cache_key) is None:
        API_KEY = "7e11ad7b06ed26da80aa7710fe2a9d9e"
        link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=pt_br"
        request_weather = requests.get(link).json()
        description = request_weather['weather'][0]['description']
        temp = kelvin_to_celsius(request_weather['main']['temp'])
        icon = request_weather['weather'][0]['icon']
        weather_data = {'weather': {
            'desc': description,
            'temp': temp,
            'city': city_name,
            'icon': icon
        }}
        cache.set(cache_key, weather_data, 2 * 60 * 60)

    else:
        weather_data = cache.get(cache_key)

    return weather_data


def kelvin_to_celsius(temp):
    return round(temp - 273.15)
