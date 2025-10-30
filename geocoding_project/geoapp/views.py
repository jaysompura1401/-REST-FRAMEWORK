from django.shortcuts import render
import requests

def index(request):
    data = {'status': 'none'}
    if request.method == 'POST':
        address = request.POST.get('address')
        api_key = "13aedba836a3456cbf8edd9a69354084"  # Replace your key here
        url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
        response = requests.get(url)
        result = response.json()
        if result['results']:
            lat = result['results'][0]['geometry']['lat']
            lng = result['results'][0]['geometry']['lng']
            data = {
                'address': address,
                'latitude': lat,
                'longitude': lng,
                'status': 'success'
            }
        else:
            data = {
                'status': 'error',
                'message': 'Address not found. Please enter a valid address.'
            }
    return render(request, 'index.html', {'data': data})
