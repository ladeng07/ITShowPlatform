from django.urls import path
from . import views

# from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("department/", views.department_message.as_view()),
    path("sign_up/", views.sign_up.as_view()),
    path("sign_up/verification_code/", views.send_email.as_view()),
    # path("sign_up/<string:pk>", views.Sign_in.as_view({"get": "get"}))
]
