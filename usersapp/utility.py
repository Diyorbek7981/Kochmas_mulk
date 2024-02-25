import re
import threading
import phonenumbers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from twilio.rest import Client
from django.conf import settings

# email yoki telefon raqamiga tekshiradi ------------------------>


email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


def check_email_or_phone(email_or_phone):
    if re.fullmatch(email_regex, email_or_phone):
        email_or_phone = "email"

    elif len(email_or_phone) == 13 and email_or_phone.startswith("+998"):
        email_or_phone = 'phone'

    else:
        data = {
            "success": False,
            "message": "Kiritilgan malumot noto'g'ri"
        }
        raise ValidationError(data)

    return email_or_phone


# email username va telefon raqamini regex orqali tekshiradi---------------------->

#  Loginda kiritilgan inputni username email yoki phonega ajratib beradi
def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = 'email'

    elif re.fullmatch(phone_regex, user_input):
        user_input = 'phone'

    elif re.fullmatch(username_regex, user_input):
        user_input = 'username'

    else:
        data = {
            "success": False,
            "message": "Email, username yoki telefon raqamingiz noto'g'ri"
        }
        raise ValidationError(data)
    return user_input


# emailga codni jo'natish uchun html orqali emailiga yuborish uchun ----------->
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/acticate_account.html',
        {"code": code}
    )
    Email.send_email(
        {
            "subject": "Royhatdan otish",
            "to_email": email,
            "body": html_content,
            "content_type": "html"
        }
    )


# --------------------------------------------------------------------------------

# twilioda telefon raqamiga code yuborish ------------------------------------------->


def send_phone_code(phone, code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Salom do'stim! Sizning tasdiqlash kodingiz: {code}\n",
        from_="+15612993508",  # twiliodagi raqam
        to=f"{phone}"
    )

# # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client
#
# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#                               body='Hi there',
#                               from_='+15017122661',
#                               to='+15558675310'
#                           )
#
# print(message.sid)
