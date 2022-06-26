import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.contrib import messages
from django.shortcuts import redirect

from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)


def send(phone_number):  
   
    verify.verifications.create(to=str('+91')+phone_number, channel='sms')
   

def check(phone_number, code):
    try:
        result = verify.verification_checks.create(to=str('+91')+phone_number, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
