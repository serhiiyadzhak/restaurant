from . import views
from django.urls import path
from .views import *
from django.urls import path

    
   
from django.urls import path



urlpatterns = [
    path('api/register', RegisterAPIView.as_view(), name='login'),
    path('api/login', LoginAPIView.as_view(), name='login'),
    path('api/user', UserView.as_view(), name='user'),
    path('api/restaurant', RestaurantAPIView.as_view(), name='restaurant'),
    path('api/menu', MenuAPIView.as_view(), name='menu'),
    path('api/employee', EmployeeAPIView.as_view(), name= 'employee'),
    path('api/vote', VoteAPIView.as_view(), name='vote'),
    path('api/result', ResultAPIView.as_view(), name='result')
   
]

