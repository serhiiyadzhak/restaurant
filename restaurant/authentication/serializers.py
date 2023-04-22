from django.db.models import fields
from rest_framework import serializers
from .models import CustomUser, Restaurant, Menu, Employee, Vote
  
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'id')

class RestaurantrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'owner')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('restaurant', 'menu')

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'id', 'restaurant')      

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('day', 'menu', 'employee', 'vote')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('day', 'menu', 'vote')
