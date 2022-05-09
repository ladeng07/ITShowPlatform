from django.urls import path
from . import views

# from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("department_cn/", views.DepartmentMessageView.as_view()),
    path("sign_up/", views.SignUpView.as_view()),
    path("sign_up/verification_code/", views.SendEmailView.as_view()),
    # path("sign_up/<string:pk>", views.Sign_in.as_view({"get": "get"}))
]
