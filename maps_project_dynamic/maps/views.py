from django.shortcuts import render, redirect
from django.conf import settings
from .models import Doctor
from .forms import DoctorForm
import requests

def index(request):
    doctors = Doctor.objects.order_by('-created_at')[:10]
    return render(request, 'maps/index.html', {'doctors': doctors})

def add_doctor(request):
    message = None
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            # geocode using OpenCage
            address = f"{doc.address}, {doc.city}" if doc.city else doc.address
            key = settings.OPENCAGE_API_KEY
            try:
                resp = requests.get('https://api.opencagedata.com/geocode/v1/json', params={'q': address, 'key': key, 'limit':1, 'no_annotations':1}, timeout=10)
                data = resp.json()
                if data.get('results'):
                    geom = data['results'][0]['geometry']
                    doc.latitude = geom.get('lat')
                    doc.longitude = geom.get('lng')
                else:
                    message = 'Geocoding returned no results. Please check the address.'
            except Exception as e:
                message = f'Error contacting OpenCage: {e}'
            doc.save()
            return redirect('map')
    else:
        form = DoctorForm()
    return render(request, 'maps/add_doctor.html', {'form': form, 'message': message})

def map_view(request):
    doctors = list(Doctor.objects.exclude(latitude__isnull=True, longitude__isnull=True).values('name','specialty','address','city','latitude','longitude'))
    return render(request, 'maps/map.html', {'doctors': doctors})
