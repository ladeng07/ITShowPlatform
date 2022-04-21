from django.contrib import admin
from django.urls import path, include
from . import views

# from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("department/", views.Department_message.as_view()),
    path("sign_up/", views.Sign_up.as_view()),
    path("sign_up/verification_code/", views.Send_email.as_view()),
    # path("sign_up/<string:pk>", views.Sign_in.as_view({"get": "get"}))
]

# router = DefaultRouter()
# router.register("sign_in", views.Sign_in, "sign_in")
# urlpatterns += router.urls
