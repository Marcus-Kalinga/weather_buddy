from django.urls import path
from .views import home_view, search_history_view
urlpatterns= [
          path("", home_view, name= "home"),
          path("history/", search_history_view, name="home"),
          ]
