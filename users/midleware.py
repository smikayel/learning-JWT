import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JWT_midleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.WHITELISTED_URLS = [
        '/api/v1/user/auth',
        '/api/v1/user',
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
            except:
                return JsonResponse({'data': "Authorization Header is missing!"}, status=403)
            if response.path.split('/')[-2] == "poll":
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
                print(e)
                return JsonResponse({'data': "Forbidden"}, status=403)
        return self.get_response(response)
     