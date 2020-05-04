from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('detail/<city_name>/', views.detail_city, name='detail_city'),
]
