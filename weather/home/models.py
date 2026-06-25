# Create your models here.
# weather/models.py
from django.db import models


class WeatherSearches(models.Model):
    """
    Model to store weather search history.
    Each record represents one search query made by a user.
    """
    # City name (max length 100 characters to accommodate long city names)
    city = models.CharField(max_length=100)
    
    # Weather data fields
    temperature = models.FloatField(default=0.0)  # Temperature in Celsius
    feels_like = models.FloatField(default=0.0)   # Feels-like temperature in Celsius
    condition = models.CharField(max_length=100, default="none")  # Weather condition (e.g., "Sunny", "Rainy")
    humidity = models.IntegerField(default=0)   # Humidity percentage
    wind_speed = models.FloatField(default=0.0)   # Wind speed in km/h
    pressure = models.FloatField(default=0.0)     # Atmospheric pressure in mb
    
    # Auto-populated timestamp - this is the key for your "date and time of search"
    # auto_now_add=True sets the field to current time when the record is created
    searched_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: You could also add a user field here if you implement user authentication
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        # Order by most recent searches first (descending order)
        ordering = ['-searched_at']
        # Human-readable name for the model in admin interface
        verbose_name_plural = "Weather Searches"
    
    def __str__(self):
        """
        String representation of the model.
        Useful for display in admin panel and debugging.
        """
        return f"{self.city} - {self.searched_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def get_recent_searches(cls, limit=10):
        """
        Helper method to get recent searches.
        Returns the most recent 'limit' number of searches.
        You can use this in your views to display search history.
        
        Example usage in views:
        recent_searches = WeatherSearches.get_recent_searches(5)
        """
        return cls.objects.all()[:limit]
