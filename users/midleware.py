import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JWT_midleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.WHITELISTED_URLS = [
        '/api/v1/user/auth',
         ]
        self.ADMIN_URLS = [
            '/api/v1/user'
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
            #check Permissions
            if not token:
                return JsonResponse({'data': "Unauthenticated!"}, status=403)
            try:
                payload = jwt.decode(token, 'secret', algorithms=["HS256"])
                # request  = response.GET.copy()
                request = self.get_response(response)
                print(response.method)
                if response.method == "GET" or response.method == "DELETE":
                    if self.checkGETpermissions(payload["uuid"], payload["isAdmin"], response.path):
                        return request
                    else:
                        return JsonResponse({'data': "Forbidden!"}, status=403)   
                return request
            except Exception as e:
                print(e)
                response = JsonResponse({'data': "Wrong token!"}, status=403)
                return response
        return self.get_response(response)
     