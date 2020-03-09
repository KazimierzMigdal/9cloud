from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<city_name>/', views.detail_city, name='test-detail_city'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
]
