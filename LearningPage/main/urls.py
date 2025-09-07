from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("item/<int:item_id>/", views.item_view, name="item_view")
]
