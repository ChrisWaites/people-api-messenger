from flask import Flask, request
from pymessenger.bot import Bot
import os 

import people

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

LOGIN_URL = 'https://people-api-server.herokuapp.com/auth/login/?next=/'
SERVER_URL = 'https://people-api-server.herokuapp.com/'

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global count
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'
    else: # POST
        req = request.get_json()
        for event in req.get('entry'):
            messaging = event.get('messaging')
            for message in messaging:
                if message.get('message'):
                    recipient_id = message.get('sender').get('id')
                    text = message.get('message').get('text')

                    try:
                        if text == 'login':
                            bot.send_button_message(
                                recipient_id, 
                                'Login', {
                                    'type': 'account_link',
                                    'url': LOGIN_URL,
                                })

                        elif text == 'logout':
                            bot.send_button_message(
                                recipient_id, 
                                'Logout', {
                                    'type': 'account_unlink',
                                })

                        else:
                            raise Exception()
                    except Exception as e:
                        print(e)
                        bot.send_text_message(recipient_id, 'Sorry, something must have gone wrong.')

    return "Message processed"

if __name__ == "__main__":
    app.run()
