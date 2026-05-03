from django.urls import path
from .views import BookView
from .views import GetView
from .views import CancelView
from .views import HandleView

urlpatterns = [
    path('book/', BookView.as_view()),
    path('get/<str:id>/', GetView.as_view()),
    path('cancel/<str:id>/', CancelView.as_view()),
    path('handle/<str:id>/', HandleView.as_view()),
]