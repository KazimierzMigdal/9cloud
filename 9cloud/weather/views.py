from .forms import CityForm
from .models import City
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
import requests


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    messages.error(request, f'City deleted successfully!')
    return redirect('index')


def detail_city(request, city_name):
    cities = City.objects.all().order_by('-id')
    city = City.objects.get(name=city_name)
    source = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    data = requests.get(source.format(city)).json()
    source_detail = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    data_detail = requests.get(source_detail.format(city)).json()

    forecast = City.objects.get_forecast(data_detail)

    #forecast
    days, tempertures, rains = [], [], []
    list_data = data_detail['list']
    for day_data in range(len(list_data)):
        date_data = list_data[day_data]
        day = date_data['dt_txt']
        day_object = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
        day_str=day_object.strftime("%H:%M")
        days.append(day_str)
        temperture = date_data['main']['temp']
        tempertures.append(temperture)
        if 'rain' in date_data.keys():
            if '1h' in date_data['rain'].keys():
                 rain = date_data['rain']['1h']
            elif '3h' in date_data['rain'].keys():
                rain = date_data['rain']['3h']
            else:
                rain = 0
        else:
            rain = 0
        rains.append(rain)
    #time period for forecast
    days=days[:9]
    tempertures = tempertures[:9]
    rains=rains[:9]

    #detail_informations
    clouds = data['clouds']['all']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    icon =  data['weather'][0]['icon']
    pressure = data['main']['pressure']
    temperature = data['main']['temp']
    windspead = data['wind']['speed']

    direction_symbol_list = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'E']
    if 'deg' in data['wind'].keys():
        direction = data['wind']['deg']
    else:
        direction=0
    wind_direction_grup= int((float(direction)+22.5)/45)
    wind_direction_symbol = direction_symbol_list[wind_direction_grup]

    weather_date = {'city': city,
                'clouds': clouds,
                'description': description,
                'humidity': humidity,
                'icon': icon,
                'pressure': pressure,
                'temperture': temperature,
                'windspead': windspead,
                'wind_direction_symbol': wind_direction_symbol,
                }
    weather_date.update(forecast)

    context = {'weather_date': weather_date, 'cities': cities}

    return render(request, 'weather/detail.html', context)


def index(request):
    cities = City.objects.all().order_by('-id')
    source = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    weather_date = []

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                data = requests.get(source.format(new_city)).json()
                if data['cod'] == 200:
                    form.save()
                    messages.success(request, f'City added successfully!')
                else:
                    messages.error(request, f'City does not exist in the world!')
            else:
                messages.warning(request, f'City already exists in the database!')

    form = CityForm()

    for city in cities:
        data=requests.get(source.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperture': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']}
        weather_date.append(city_weather)

    context = {'cities': cities,
            'form': form,
            'weather_date': weather_date}

    return render(request, 'weather/index.html', context)
