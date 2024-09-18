from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('locations/', views.locations_view, name='locations'),
    path('owners/', views.owner_view, name='owners'),
    path('employees/', views.employee_view, name='employees'),
    path('services/', views.services_view, name='services'),
    path('employments/', views.employments_view, name='employments'),
    path('drones/', views.drones_view, name = 'drones'),
    path('payload/', views.payload_view, name = 'payload'),
    path('pilots/', views.pilots_view, name = 'pilots'),
    path('ingredient_table/', views.ingredient_table_view, name = 'ingredient_table'),
    path('ingredient_view/', views.ingredient_view, name = 'ingredient_view'),
    path('restaurants/', views.restaurants_view, name='restaurants'),
]
