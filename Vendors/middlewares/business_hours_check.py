from django.http import HttpResponse
from datetime import datetime, time

class BusinessHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # check if the current time is within business hours
        now = datetime.now().time()
        business_hours_start = time(hour=9, minute=0)
        business_hours_end = time(hour=17, minute=0)
        if now < business_hours_start or now >= business_hours_end:
            return HttpResponse('Sorry, we are currently closed. Please come back during our business hours.')

        return response