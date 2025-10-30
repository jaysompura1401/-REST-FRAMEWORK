from django.shortcuts import render
import json
import urllib.request

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST['city']
        api_key = "8a6d624b99bfb394cf452268fafbed04"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)
            if list_of_data.get('cod') != 200:
                data = {'error': list_of_data.get('message', 'City not found!')}
            else:
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                    "temp": str(round(list_of_data['main']['temp'] - 273.15, 2)) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                }
        except Exception as e:
            data = {'error': str(e)}

    return render(request, "main/index.html", data)
