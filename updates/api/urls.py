from django.urls import path

from .views import (
    UpdateModelDetailAPIView,
    UpdateModelListAPIView
)

app_name = 'updates.api'
urlpatterns = [
    path('', UpdateModelListAPIView.as_view()),
    path('<int:pk>/', UpdateModelDetailAPIView.as_view()),
]
