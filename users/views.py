from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Poll, userPoll
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
import uuid, json
import jwt, datetime


class UserAPIView(APIView):
    def get(self, request):
        """
        get request to get all users
        Autentication needed
        """
        lst = User.objects.all().values()
        return JsonResponse({'data': list(lst)}, status = 200)
       
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
        User.objects.filter(pk=request.data["uuid"]).delete()
        try:
            return Response({'data': "deleted"})
        except:
            return Response({'data': "Something went wrong..."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        """
        password changing, 
        Here user ned to be logined, anyway password changing is forbidden.
        """
        try:
            updated = User.objects.filter(pk=request.data["uuid"]).update(password=request.data["new_password"])
            return Response({'updated': updated})
        except:
            return Response({"data": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

class UserAuthAPIView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
       
        try:
            user = User.objects.filter(username=username).values().get()
            if password != user["password"]:
                response = JsonResponse({"data": "wrong password"},status=403)
                return response

            payload = {
                "uuid": user["uuid"],
                "username": user["username"],
                "isAdmin": user["isAdmin"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = JsonResponse(payload,status=200)
            response['Authorization'] = token
            return response
        except:
            return JsonResponse({"data": "", "error": "User not found!"}, status=404)


class PollCRUD(APIView):
    def post(self, request):
       
        try:
            token = request.headers["Authorization"]
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            creator = User.objects.get(uuid=payload["uuid"])
            createdPOLL = Poll.objects.create(
                uuid=uuid.uuid1(),
                title =  request.data["title"],
                firstOption = request.data["firstOption"],
                secondOption = request.data["secondOption"],
                startDate = datetime.datetime.utcnow(),
                endDate = datetime.datetime.utcnow(),
                creator = creator
            )
            return  JsonResponse(model_to_dict(createdPOLL), status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"data": "", "error": "Something went wrong"}, status=500)

    def put(self, request):
        try:
            updated = Poll.objects.filter(pk=request.data["poll-uuid"]).update(title=request.data["title"])
            return Response({'updated': updated})
        except:
            return Response({"data": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    
    def get(self, request):
        lst = Poll.objects.all().values()
        return JsonResponse({'data': list(lst)}, status = 200)

    def delete(self, request):
        Poll.objects.filter(pk=request.data["poll-uuid"]).delete()
        try:
            return Response({'data': "deleted"})
        except:
            return Response({'data': "Something went wrong..."}, status=status.HTTP_403_FORBIDDEN)

def getVoted(request):
    if request.method == "GET":
        lst = userPoll.objects.all().values()
        return JsonResponse({'data': list(lst)}, status = 200)

def vote_fore_one(request, poll_uuid_slug):
    if request.method == "PUT":
        try:
            token = request.headers["Authorization"]
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            print(token)
            creator = User.objects.get(uuid=payload["uuid"])
            poll = Poll.objects.filter(uuid=poll_uuid_slug).values().get()
            if json.loads(request.body)["option-id"] == 1:
                votedPoll =  Poll.objects.filter(uuid=poll_uuid_slug).update(firstOptionVoteCount=int(poll["firstOptionVoteCount"]) + 1)
            else:
                votedPoll =  Poll.objects.filter(uuid=poll_uuid_slug).update(secondOptionVoteCount=int(poll["secondOptionVoteCount"]) + 1)
            voted = Poll.objects.get(uuid=poll_uuid_slug)
            userPoll.objects.create(
                poll = voted,
                voted = creator
            )
            return JsonResponse({"data": votedPoll, "error": ""}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"data": "", "error": "Not found!"}, status=404)
    return JsonResponse({"data": "", "error": "Something went wrong"}, status=500)

def get_with_pagination(request, pagination_poll_query):
    if request.method != "GET":
        return JsonResponse({'Forbidden request': list(lst)}, status = 500)
    start = pagination_poll_query.split('-')[0]
    end = pagination_poll_query.split('-')[1]

    if start and end:
        lst = Poll.objects.all().values()[int(start): int(end) + 1]
        return JsonResponse({'data': list(lst)}, status = 200)
    else:
        return JsonResponse({'Unrecognized query': pagination_poll_query}, status = 404)
