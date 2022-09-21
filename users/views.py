from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework import generics
from rest_framework.views import APIView


class UserAPIView(APIView):
    def get(self, request):
        lst = User.objects.all().values()
        return Response({'posts': list(lst)})

    def post(self, request):
        post_new = User.objects.create(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            isAdmin=False
        )
        return Response({'post': model_to_dict(post_new)})

    def delete(self, request):
        deleted = User.objects.filter(pk=request.data["uuid"]).delete()
        return Response({'post': "deleted"})
    
    def put(self, request):
        updated = User.objects.filter(pk=request.data["username"])
        updated.update(username=request.data["username"])
        return Response({'post': model_to_dict(updated)})