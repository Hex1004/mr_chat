from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class CookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user has already accepted or rejected cookies
        cookie_consent = request.COOKIES.get('cookie_consent')

        # If no cookie is found, set the flag to show cookie popup
        if cookie_consent is None:
            request.show_cookie_popup = True
        else:
            request.show_cookie_popup = False
