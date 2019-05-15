from django.conf.urls import url, include

from rest_framework import routers

from . import views

starship_router = routers.DefaultRouter()
starship_router.register(r'starships', views.StarshipView)

urlpatterns = [
    url(r'^', include(starship_router.urls)),
]
