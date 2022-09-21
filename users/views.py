from turtle import update
from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
import uuid
from .helpers import pass2hash


class UserAPIView(APIView):
    def get(self, request):
        lst = User.objects.all().values()
        return Response({'data': list(lst)})

    def post(self, request):
        try:
            post_new = User.objects.create(
                uuid=uuid.uuid1(),
                username=request.data['username'],
                email=request.data['email'],
                password=pass2hash(request.data['password']),
                isAdmin=False
            )
            return Response({'data': model_to_dict(post_new)})
        except:
            return Response({'data': "something went wrong choose another username or email"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        try:
            User.objects.filter(pk=request.data["uuid"]).delete()
            return Response({'data': "deleted"})
        except:
            return Response({'data': "Something went wrong..."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        try:
            updated = User.objects.filter(pk=request.data["uuid"]).update(password=pass2hash(request.data["new_password"]))
            return Response({'updated': updated})
        except Exception as e:
            print(e)
            return Response({"data": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
