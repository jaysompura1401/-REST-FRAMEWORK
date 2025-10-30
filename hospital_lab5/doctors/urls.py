from django.urls import path
from .views import DoctorListCreateAPIView

urlpatterns = [
    path('doctors/', DoctorListCreateAPIView.as_view(), name='doctor-list-create'),
]
