from django.urls import path
from .views import LoginView, UserView, RetrieveUpdateUserView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/<int:pk>/", RetrieveUpdateUserView.as_view()),
]
