from django.urls import path

from .views import RegisterView
from .views import UpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('update/<str:id>/', UpdateView.as_view()),
]