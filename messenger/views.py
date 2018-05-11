from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import people
import json
from pymessenger.bot import Bot


bot = Bot(settings.ACCESS_TOKEN)

LOGIN_URL = 'https://people-api-server.herokuapp.com/social-login/'
REGISTER_URL = 'https://people-api-server.herokuapp.com/register/'


@csrf_exempt
def index(request):
    try:

        if request.method == 'GET':
            token_sent = request.args.get("hub.verify_token")
            if token_sent == settings.VERIFY_TOKEN:
                return request.args.get("hub.challenge")
            return HttpResponse('Invalid verification token.')

        else: 
            req = json.loads(request.body)

            for event in request.get('entry'):
                messaging = event.get('messaging')
                for message in messaging:
                    if message.get('message'):

                        recipient_id = message.get('sender').get('id')
                        text = message.get('message').get('text')

                        if text == 'help':
                            bot.send_text_message(recipient_id, 'Commands:\n\nregister\nlogin\nlogout')
                            
                        elif text == 'register':
                            bot.send_button_message(
                                recipient_id, 'Click here to register.', [{
                                        'type': 'web_url',
                                        'url': REGISTER_URL,
                                        'title': 'Register',
                                    }]
                                )

                        elif text == 'login':
                            bot.send_button_message(
                                recipient_id, 'Click here to login.', [{
                                        'type': 'account_link',
                                        'url': LOGIN_URL,
                                    }]
                                )

                        elif text == 'logout':
                            bot.send_button_message(
                                recipient_id, 'Click here to logout.', [{
                                        'type': 'account_unlink'
                                    }]
                                )

                        else:
                            bot.send_text_message(recipient_id, 'Sample Query? [1-5]')

    except Exception as e:
        print(e)

    return HttpResponse('Message processed.')

