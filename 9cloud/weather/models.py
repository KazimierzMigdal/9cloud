from datetime import datetime
from django.db import models


class CityMenager(models.Manager):
    def get_forecast(self, data_detail):
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

        # clouds = data['clouds']['all']
        # description = data['weather'][0]['description']
        # humidity = data['main']['humidity']
        # icon =  data['weather'][0]['icon']
        # pressure = data['main']['pressure']
        # temperature = data['main']['temp']
        # windspead = data['wind']['speed']

        # direction_symbol_list = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'E']
        # if 'deg' in data['wind'].keys():
        #     direction = data['wind']['deg']
        # else:
        #     direction=0
        # wind_direction_grup= int((float(direction)+22.5)/45)
        # wind_direction_symbol = direction_symbol_list[wind_direction_grup]

        forecast = {'date': days,
                'rains': rains,
                'temperatures': tempertures,
                }

        return forecast


class City(models.Model):
    name = models.CharField(max_length=25)
    objects = CityMenager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_city',kwargs={'pk':self.pk})

    class Meta:
        verbose_name_plural = 'cities'
