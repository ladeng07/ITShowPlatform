from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.comments.as_view()),
]


