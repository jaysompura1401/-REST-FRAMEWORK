from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer

# List all doctors or create a new doctor
class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

# Retrieve, update, or delete a specific doctor by ID
class DoctorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
