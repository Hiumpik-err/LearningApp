from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.home, name="home"),
    path('profile', views.profile, name="profile"),
    path("create/<str:type>/", views.create_item , name="create_item"),
    path("item_view/<str:type>/<int:id>", views.item_view, name="item_view"),
    path("available_articles/<str:category>", views.available_articles, name="available_articles"),
    path("available_courses/<str:category>", views.available_courses, name="available_courses"),
    path("available_quizzes/<str:category>", views.available_quizzes, name="available_quizzes"),
]


