import stat
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

import jwt, datetime


class UserAPIView(APIView):
    def get(self, request):
        """
        get request to get all users
        Autentication needed
        """

        token = request.COOKIES.get('jwt')
        if not token:
            Response({'data': "Unauthenticated!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            if not payload:
                return Response({'data': "Wrong token!"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'data': "Wrong token!"}, status=status.HTTP_403_FORBIDDEN)
        
        lst = User.objects.all().values()
        return Response({'data': list(lst)})
       
    def post(self, request):
        """
        post request for creating user ,(IsAdmin will be False(default))
        Autentication not needed 
        """
        try:
            post_new = User.objects.create(
                uuid=uuid.uuid1(),
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                isAdmin=False
            )
            return Response({'data': model_to_dict(post_new)})
        except:
            return Response({'data': "something went wrong choose another username or email"}, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request):
        """
        delete request for deleting user needs isAdmin true
        Autentication needed
        """
        token = request.COOKIES.get('jwt')
        if not token:
            Response({'data': "Unauthenticated!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except:
            return Response({'data': "Wrong token!"}, status=status.HTTP_403_FORBIDDEN)
        if payload["isAdmin"]:
            try:
                User.objects.filter(pk=request.data["uuid"]).delete()
                return Response({'data': "deleted"})
            except:
                return Response({'data': "Something went wrong..."}, status=status.HTTP_403_FORBIDDEN)
        return Response({'data': "Not enough permissions"}, status=status.HTTP_403_FORBIDDEN)



    def put(self, request):
        """
        password changing, 
        Here user ned to be logined, anyway password changing is forbidden.
        """
        token = request.COOKIES.get('jwt')
        if not token:
            Response({'data': "Unauthenticated!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except:
            return Response({'data': "Wrong token!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            updated = User.objects.filter(pk=payload["uuid"]).update(password=request.data["new_password"])
            return Response({'updated': updated})
        except:
            return Response({"data": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class UserAuthAPIView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        # try:
        user = User.objects.filter(username=username).values().get()
        if password != user["password"]:
            return Response({"data": "wrong password"}, status=status.HTTP_403_FORBIDDEN)
        payload = {
            "uuid": user["uuid"],
            "username": user["username"],
            "isAdmin": user["isAdmin"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserLogoutView(APIView):
    """
    Logout request
    """
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            Response({'data': "Unauthenticated!"}, status=status.HTTP_403_FORBIDDEN)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

