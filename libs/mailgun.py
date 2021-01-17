import os
from typing import List
from requests import Response, post


class MailgunException(Exception) :
    def __init__(self, message: str) :
        self.message = message


class Mailgun :

    FROM_TILE = 'Pricing Service'
    FROM_EMAIL = 'do-not-reply@sandbox44bbee09161f4042b348138bb6b5c680.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response :
        api_key = os.environ.get('MAILGUN_API_KEY')
        domain = os.environ.get('MAILGUN_DOMAIN')

        if api_key is None :
            raise MailgunException('Failed to load Mailgun API KEY')
        if domain is None :
            raise MailgunException('Failed to load MAILGUN Domain')
        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={
                            "from" : f"{cls.FROM_TILE} <{cls.FROM_EMAIL}>",
                            "to" : email,
                            "subject" : subject,
                            "text" : text,
                            "html" : html})
        if response.status_code != 200 :
            print(response.json())
            raise MailgunException('An error occurred while sending email')
        return response

