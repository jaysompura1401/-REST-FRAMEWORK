from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer

# API to handle both GET and POST requests
class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
