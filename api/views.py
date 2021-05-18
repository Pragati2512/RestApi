from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework import permissions,viewsets, status , generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
#from rest_framework.parsers import JSONParser

from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import EmployeeSerializer, DepartmentSerializer, RegisterSerializer, LoginSerializer
from .models import User, employee, department



class Departments(viewsets.ModelViewSet):
    queryset = department.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET' ])
def emp_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    all_employees = employee.objects.all()
    paginated_emp = paginator.paginate_queryset(all_employees, request)
    serializer = EmployeeSerializer(paginated_emp , many=True)
    return  paginator.get_paginated_response(serializer.data)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {'username': request.data.get('username', ""), 'password': request.data.get('password', "")}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = authenticate(username=data["username"], password=data["password"])
            login(request, user)
            return Response('You are logged in successfully!!!', status=status.HTTP_200_OK)
        return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register(request):
    serializer = RegisterSerializer
    data1 ={}
    if request.method == 'POST':
        data1 = {'username': request.data.get('username', ""), 'email': request.data.get('email', ""), 'name': request.data.get('name', ""),
            'password': request.data.get('password', ""), 'join': request.data.get('join', "2021-05-10"), 'dob': request.data.get('dob', "1990-01-01"),
            'phone': request.data.get('phone', ""), 'dept': request.data.get('dept', ""), 'address': request.data.get('address', ""),}
        #data1 = JSONParser().parse(request)
        print(data1)
        serializer = RegisterSerializer(data=data1)
        if serializer.is_valid():
            print("Valid toh hai")
            user1 = User.objects.create(username=data1['username'], email=data1['email'])
            user1.set_password(data1['password'])
            user1.save()
            dept1 = department.objects.get(id=data1['dept'])
            employee1 = employee(user=user1, name=data1['name'], department =dept1 , phone = data1['phone'],
                        joining_date = data1['join'], dob = data1['dob'], address = data1['address'])
            employee1.save()
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #return Response(serializer.data , status=200)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_details(request):
    emp1 = employee.objects.get(user=request.user)
    serializer = EmployeeSerializer(emp1 , data=request.data, partial=True)
    if request.method == 'PATCH':
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data ,status=status.HTTP_200_OK )


'''
class RegisterView(APIView):
    queryset = employee.objects.all()
    permission_classes = (IsAdminUser)
    serializer_class = RegisterSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
