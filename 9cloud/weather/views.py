import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.http import HttpResponse
from datetime import datetime

def chartjs(request):
    return render(request, 'weather/chartjs.html', {})
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'

            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'danger'
        else:
            message = 'City added successfully!'
            message_class = 'success'

    form = CityForm()
    cities = City.objects.all().order_by('-id')


    weather_date = []
    cities_names = []
    for city in cities:
        r=requests.get(url.format(city)).json()
        cities_names.append(city.name)
        city_weather = {
            'city': city.name,
            'temperture': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_date.append(city_weather)


    context = {'weather_date': weather_date, 'form': form, 'message': message, 'message_class': message_class, 'cities_names': cities_names}
    return render(request, 'weather/index_test.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('test')


def detail_city(request, city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'


    city = City.objects.get(name=city_name)
    r=requests.get(url.format(city)).json()
    l=requests.get(url2.format(city)).json()
    days = []
    tempertures = []
    rains = []
    cities_names = []

    for town in City.objects.all():
        cities_names.append(town.name)

    list_data = l['list']
    for day_data in range(len(list_data)):
        data = list_data[day_data]

        day = data['dt_txt']
        day_date_object = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
        str_day=day_date_object.strftime("%H:%M")
        days.append(str_day)

        temperture = data['main']['temp']
        tempertures.append(temperture)
        if 'rain' in data.keys():
            if '1h' in data['rain'].keys():
                 rain = data['rain']['1h']
            elif '3h' in data['rain'].keys():
                rain = data['rain']['3h']
            else:
                rain = 0
        else:
            rain = 0
        rains.append(rain)

    if 'deg' in r['wind'].keys():
        direction = r['wind']['deg']
    else:
        direction=0

    rains=rains[:9]
    days=days[:9]
    tempertures = tempertures[:9]

    direction_symbol_list = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'E']
    direction_grup= int((float(direction)+22.5)/45)
    direction_symbol = direction_symbol_list[direction_grup]

    weather_date = {'city': city,
                'temperture': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'windspead': r['wind']['speed'],
                'winddirection': direction,
                'direction_symbol': direction_symbol,
                'clouds': r['clouds']['all'],
                'pressure': r['main']['pressure'],
                'humidity': r['main']['humidity'],
                'date': days,
                'temperatures': tempertures,
                'rains': rains,
                }

    print(weather_date['city'])

    context = {'weather_date': weather_date, 'cities_names': cities_names,
                }

    return render(request, 'weather/detail_test.html', context)

