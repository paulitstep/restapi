from django.urls import path

from .views import StatusAPIView, StatusAPIDetailView


app_name = 'status.api'
urlpatterns = [
    path('', StatusAPIView.as_view(), name='list'),
    path('<int:pk>', StatusAPIDetailView.as_view(), name='detail'),
]
