"""
Main URL configuration for the project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line tells the project to look at your expenses app for any URLs starting with 'api/'
    path('api/', include('expenses.urls')), 
]
