from datetime import datetime
from django.db import models


class CityMenager(models.Manager):
    def get_forecast(self, forecast_data, period):
        days, tempertures, rains = [], [], []
        list_data = forecast_data['list']
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

        days=days[:period]
        tempertures = tempertures[:period]
        rains=rains[:period]

        return {'date': days,
                'rains': rains,
                'temperatures': tempertures
                }


    def get_weather_data(self, detail_data):
        city = detail_data['name']
        clouds = detail_data['clouds']['all']
        description = detail_data['weather'][0]['description']
        humidity = detail_data['main']['humidity']
        icon =  detail_data['weather'][0]['icon']
        pressure = detail_data['main']['pressure']
        temperature = detail_data['main']['temp']
        windspead = detail_data['wind']['speed']

        direction_symbol_list = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'E']
        if 'deg' in detail_data['wind'].keys():
            direction = detail_data['wind']['deg']
        else:
            direction=0
        wind_direction_grup= int((float(direction)+22.5)/45)
        wind_direction_symbol = direction_symbol_list[wind_direction_grup]

        return {'city': city,
                'clouds': clouds,
                'description': description,
                'humidity': humidity,
                'icon': icon,
                'pressure': pressure,
                'temperture': temperature,
                'windspead': windspead,
                'wind_direction_symbol': wind_direction_symbol
                }


class City(models.Model):
    name = models.CharField(max_length=25)
    objects = CityMenager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_city',kwargs={'pk':self.pk})

    class Meta:
        verbose_name_plural = 'cities'
