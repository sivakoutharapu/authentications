from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import viewsets
from .models import covid
from .serializers import covidSerializers,userSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class userRegister(APIView):
    def post(self, request):
        serializer = userSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(username = serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({"status": 200, "data":serializer.data, "token": str(token_obj)})
    

class covidView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        covid_cases = covid.objects.all()
        serializers = covidSerializers(covid_cases, many=True)
        print(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializers = covidSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    def put(self, request,id):
        try:
            covid_data = covid.objects.get(pk=id)
            serializers = covidSerializers(covid_data, data=request.data, partial=True)
            
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_205_RESET_CONTENT)
        except covid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
            
    def delete(self, request,id):
        try:
            covid_data = covid.objects.get(pk=id)
            covid_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except covid.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
    