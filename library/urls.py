from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListBookViewset

router = DefaultRouter(trailing_slash=False)
router.register("", ListBookViewset, basename='books')

urlpatterns = [
    path('', include(router.urls)),
]