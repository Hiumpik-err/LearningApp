from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.home, name="home"), 
    path('profile', views.profile, name="profile"),
    path("profile/update", views.profile_update, name="profile_update"),
    path('search', views.search, name="search"),
    path('content_view/<str:type>/', views.content_view, name="content_view_element"),
    path("create/<str:type>/", views.create_item , name="create_item"),
    path("update/<str:type>/<int:id>", views.update, name="update"),
    path("item_view/<str:type>/<int:id>", views.item_view, name="item_view"),

]


