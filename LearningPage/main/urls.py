from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.home, name="home"), 
    path('content_view', views.content_view, name="content_view"),
    path('content_view/articles/', views.content_view, {'content_type': 'articles'}, name="content_view_articles"),
    path('content_view/tasks/', views.content_view, {'content_type': 'tasks'}, name="content_view_tasks"),
    path('content_view/quizzes/', views.content_view, {'content_type': 'quizzes'}, name="content_view_quizzes"),
    path('profile', views.profile, name="profile"),
    path("create/<str:type>/", views.create_item , name="create_item"),
    path("update/<str:type>/<int:id>", views.update, name="update"),
    path("item_view/<str:type>/<int:id>", views.item_view, name="item_view"),
    path("available_articles/<str:category>", views.available_articles, name="available_articles"),
    path("available_courses/<str:category>", views.available_courses, name="available_courses"),
    path("available_quizzes/<str:category>", views.available_quizzes, name="available_quizzes"),
]


