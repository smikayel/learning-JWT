from http.client import HTTPResponse
import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json

class JWT_midleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.WHITELISTED_URLS = [
        '/api/v1/user/auth',
        '/api/v1/user',
        '/api/v1/poll'
        ]

    def checkGETpermissions(self, uuid, isAdmin, path):
        if path in self.ADMIN_URLS and isAdmin == True:
            return True
        return False 
    
    def __call__(self, response):
        if not response.path in self.WHITELISTED_URLS:
            #check Authorization
            try:
                token = response.headers["Authorization"]
            except Exception as e:
                return JsonResponse({'data': "Authorization Header is missing!"}, status=403)
            
            if response.path.split('/')[-2] == "poll" \
                or response.path.split('/')[-1] == "home-pages-count" \
                    or response.path.split('/')[-2] == "pagination":
                return self.get_response(response)
            #check Permissions
            if not token:
                return JsonResponse({'data': "Unauthenticated!"}, status=403)
            try:
                payload = jwt.decode(token, 'secret', algorithms=["HS256"])
                if payload["isAdmin"] == True:
                    return self.get_response(response)
                return JsonResponse({'data': "Forbidden"}, status=403)
            except Exception as e:
                return JsonResponse({'data': "Forbidden"}, status=403)
        return self.get_response(response)
     