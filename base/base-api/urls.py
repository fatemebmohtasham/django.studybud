from django.urls import path
from . views_api import get_rooms,get_room



urlpatterns =[

    path('rooms/', get_rooms ,name='api_get_rooms'),
    path('room/<str:pk>', get_room ,name='api_get_room'),

    
]
