from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'starships', views.StarshipView)
router.register(r'listings', views.ListingView)

urlpatterns = [
    url(r'^', include(router.urls)),
]
