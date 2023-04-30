from django.shortcuts import render
from .models import User, ZipCode
import json
from django.http import JsonResponse
import requests

def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['username']
        
        user_instance, _ = User.objects.get_or_create(name=name)
        zip_codes = ZipCode.objects.filter(user=user_instance)
        
        weather_data = []
        for zipcode in zip_codes:
            api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode.zip_code}&appid=108a6148ab648d4232f4dfbacb361398")
            temp = api_request.json()['main']['temp']
            temp = (temp - 273.15) * 9/5 + 32
            weather_data.append({
                'zip_code': zipcode.zip_code,
                'temp': temp,
            })

        return JsonResponse({'result': weather_data, 'status': 200}, status=200)
    return render(request, 'weather/index.html')

def weather(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['username']
        zip_code = data['zip']

        user_instance, _ = User.objects.get_or_create(name=name)

        api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid=108a6148ab648d4232f4dfbacb361398")
        if api_request.json()['cod'] == '404':
            return JsonResponse({'result': 'Zip not found', 'status': 404}, status=404)

        if ZipCode.objects.filter(user=user_instance, zip_code=zip_code).exists():
            return JsonResponse({'result': 'Zip code already associated with the user', 'status': 400}, status=400)

        zipcode_instance = ZipCode.objects.create(user=user_instance, zip_code=zip_code)
        zipcode_instance.save()

        zip_codes = ZipCode.objects.filter(user=user_instance)

        weather_data = []
        for zipcode in zip_codes:
            api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode.zip_code}&appid=108a6148ab648d4232f4dfbacb361398")
            temp = api_request.json()['main']['temp']
            temp = (temp - 273.15) * 9/5 + 32
            weather_data.append({
                'zip_code': zipcode.zip_code,
                'temp': temp,
            })

        return JsonResponse({'result': weather_data, 'status': 200})
