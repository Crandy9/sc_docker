'''
COOL IDEA TO INTERCEPT ALL INCOMING REQUESTS AND VET THEM

I IMPLEMENTED AN API KEY WHICH WORKS, BUT WHOSE PURPOSE IS RENDERED
USELESS SINCE THE API KEY IS EXPOSED ON THE FRONTEND.
LEAVING THE CODE HERE AS BOILERPLATE IN CASE ANOTHER USE COMES IN THE FUTURE
'''

from django.http import JsonResponse
from sheriff_crandy_project import settings
from django.urls import resolve
# import env vars
import environ
env = environ.Env()
environ.Env.read_env()

# import logger
import logging
logger = logging.getLogger('main')


class APIKeyMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = env('API_KEY')

    def __call__(self, request):

        excluded_paths = [
            'api/sheriffcrandyadmin-6A6573757363687269737469736B696E67/',
            'api/sc/v1/token/login',
            'api/sc/v1/lctec-logout',
            'api/sc/v1/create-basic-user/',
            'api/sc/v1/delete-user-account-data/',
            'api/sc/v1/send-password-reset-link/',
            'api/sc/v1/reset-user-password/',
            '^media/(?P<path>.*)$',
        ]

        resolved_path = resolve(request.path_info).route
        # Check if the resolved path is in the excluded paths list
        if any(resolved_path.startswith(path) for path in excluded_paths):
            return self.get_response(request)
        
        api_key = request.headers.get('api-key')

        if api_key is None:
            logger.debug('api key is None')
            return JsonResponse({'error': 'Nuh uh uh. You didnt say the magic word. Nah uh uh...'}, status=403)
        
        if api_key not in self.api_key:
            logger.debug('api key: ' + str(api_key))
            return JsonResponse({'error': 'Nuh uh uh. You didnt say the magic word. Nah uh uh...'}, status=403)
        
        return self.get_response(request)