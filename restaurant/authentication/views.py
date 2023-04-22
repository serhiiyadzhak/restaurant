from .models import CustomUser, Restaurant, Menu, Employee, Vote
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.response import Response
from .serializers import ItemSerializer, LoginSerializer, RestaurantrSerializer, MenuSerializer, EmployeeSerializer, ResultSerializer, VoteSerializer
from rest_framework.views import APIView
import jwt
import datetime




class RegisterAPIView(APIView):
    serializer_class = ItemSerializer
    throttle_scope = "authentication"

    def get_queryset(self):
        users = CustomUser.objects.all()
        return users

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params["id"]
            if id != None:
                user = CustomUser.objects.get(id=id)
                serializer = ItemSerializer(user)
        except:
            users = self.get_queryset()
            serializer = ItemSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        user_data = request.data
        user = CustomUser.objects.create(username=user_data["username"],  email=user_data["email"], password=user_data["password"])
        user.save()
        user.set_password(user.password)
        serializer = ItemSerializer(user)
        return Response(serializer.data)
    
  
class RestaurantAPIView(APIView):
    serializer_class = RestaurantrSerializer 
    throttle_scope = "restaurant"
    def post(self, request, *args, **kwargs):
        data = request.data
        restaurant = Restaurant.objects.create(name=data["name"],  address=data["address"], owner=data["owner"])
        restaurant.save()
        serializer =  RestaurantrSerializer(restaurant)
        return Response(serializer.data)


class MenuAPIView(APIView):
    serializer_class = MenuSerializer 
    throttle_scope = "Menu"
    
    def post(self, request, *args, **kwargs):
        data = request.data
        req_data = request.data['restaurant']
        restaurant = Restaurant.objects.filter(id=req_data).first()
        menu = Menu.objects.create(restaurant=restaurant, menu=data["menu"])
        menu.save()
        serializer =  MenuSerializer(menu)
        return Response(serializer.data)
    



class EmployeeAPIView(APIView):
    serializer_class = EmployeeSerializer 
    throttle_scope = "Employee"

    def post(self, request, *args, **kwargs):
        user_data = request.data
        req_data = request.data['restaurant']
        restaurant = Restaurant.objects.filter(id=req_data).first()
        employee = Employee.objects.create(first_name=user_data["first_name"], last_name=user_data["last_name"], email=user_data["email"], restaurant=restaurant)
        employee.save()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)



class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found:)')  
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token.decode('utf-8')
        response = Response() 
        response.set_cookie(key='jwt', value=token, httponly=True)  #httonly - frontend can't access cookie, only for backend
        response.data = {
            'jwt token': token
        }
        return redirect("user")
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = ItemSerializer(user)
        return Response(serializer.data)
    


class VoteAPIView(APIView):
    serializer_class = VoteSerializer

    def post(self, request):
        data = request.data
        emp_data = request.data['employee']
        employee = Employee.objects.filter(id=emp_data).first()
        menu_data = request.data['menu']
        menu = Menu.objects.filter(id=menu_data).first()
        vote = Vote.objects.create(day=data["day"], employee=employee, menu=menu, vote=data["vote"])
        vote.save()
        serializer =  VoteSerializer(vote)
        return Response({'message': 'Vote recorded for version 1 of the app', 'data': serializer.data})

class ResultAPIView(APIView):
    def get(self, request):
        queryset = Vote.objects.raw("SELECT *, count(vote) FROM authentication_vote group by id  order by sum(vote) desc LIMIT 1")
        serializer = ResultSerializer(list(queryset), many=True)
        return Response(serializer.data)
