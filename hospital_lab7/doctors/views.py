from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
