from .forms import CityForm
from .models import City
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
import requests


class HomeView(ListView, FormMixin):
    model = City
    context_object_name = 'city'
    template_name = 'weather/index.html'
    form_class = CityForm

    def get_queryset(self):
        return City.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities = City.objects.all().order_by('-id')
        context['cities'] = cities
        source = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
        weather_date = []
        for city in cities:
            data=requests.get(source.format(city)).json()
            city_weather = {'city': city.name,
                        'temperture': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon']}
            weather_date.append(city_weather)
        context['weather_date'] = weather_date
        return context

    def post(self, request):
        form = CityForm(request.POST)
        source = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                data = requests.get(source.format(new_city)).json()
                if data['cod'] == 200:
                    form.save()
                    messages.success(self.request, f'City added successfully!')
                else:
                    messages.error(self.request, f'City does not exist in the world!')
            else:
                messages.warning(self.request, f'City already exists in the database!')
        return redirect('index')



def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    messages.error(request, f'City deleted successfully!')
    return redirect('index')


def detail_city(request, city_name):
    cities = City.objects.all().order_by('-id')
    city = City.objects.get(name=city_name)
    detail_source = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    detail_data = requests.get(detail_source.format(city)).json()
    forecast_source = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=9a5f969d3828fdb7109c000f855bf43c'
    forecast_data = requests.get(forecast_source.format(city)).json()

    weather_data = City.objects.get_weather_data(detail_data)
    forecast = City.objects.get_forecast(forecast_data, period=9)
    weather_data.update(forecast)

    context = {'weather_data': weather_data, 'cities': cities}

    return render(request, 'weather/detail.html', context)
