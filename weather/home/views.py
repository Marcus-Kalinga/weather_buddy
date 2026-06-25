# weather/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import WeatherSearches
import requests
from decouple import config
import os

def home_view(request):
    weather_data = None
    error_message = None
    city = None
    
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        
        if city:
            api_key = config("api_key")
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
            
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    weather_data = {
                        'city': data['location']['name'],
                        'country': data['location']['country'],
                        'temperature': data['current']['temp_c'],
                        'feels_like': data['current']['feelslike_c'],
                        'condition': data['current']['condition']['text'],
                        'humidity': data['current']['humidity'],
                        'wind_speed': data['current']['wind_kph'],
                        'pressure': data['current']['pressure_mb'],
                        'visibility': data['current']['vis_km'],
                        'uv_index': data['current']['uv'],
                        'cloud': data['current']['cloud'],
                        'sunrise': data['location']['localtime'][11:16],
                        'sunset': 'N/A',
                        'last_updated': data['current']['last_updated'],
                        'icon': data['current']['condition']['icon']
                    }
                    
                    # ***** NEW: Save the search to database *****
                    try:
                        WeatherSearches.objects.create(
                            city=weather_data['city'],
                            temperature=weather_data['temperature'],
                            feels_like=weather_data['feels_like'],
                            condition=weather_data['condition'],
                            humidity=weather_data['humidity'],
                            wind_speed=weather_data['wind_speed'],
                            pressure=weather_data['pressure']
                        )
                    except Exception as e:
                        print(f"Error saving search: {e}")  # Log error but don't break the user experience
                    
                else:
                    error_message = "City not found. Please check the spelling and try again."
                    
            except requests.exceptions.RequestException:
                error_message = "Could not connect to weather service. Please try again later."
            except KeyError:
                error_message = "Error parsing weather data. Please try again."
        else:
            error_message = "Please enter a city name."
    
    context = {
        'weather_data': weather_data,
        'error_message': error_message,
        'city': city
    }
    
    return render(request, 'home/home.html', context)




def search_history_view(request):
    """
    View function to display the search history.
    Retrieves all weather searches from the database and displays them
    in reverse chronological order (newest first).
    """
    # Get all searches ordered by newest first (this uses the ordering
    # defined in the model's Meta class)
    searches = WeatherSearches.objects.all()
    
    # Optional: You can add pagination if you have many records
    # from django.core.paginator import Paginator
    # paginator = Paginator(searches, 10)  # Show 10 searches per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    context = {
        'searches': searches,
        'total_searches': searches.count(),  # Count total number of searches
        # 'page_obj': page_obj,  # If using pagination
    }
    
    return render(request, 'home/search_history.html', context)
