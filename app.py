from flask import Flask, request
from pymessenger.bot import Bot
import os 

import people

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

global count
count = 0

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if count == 0:
                        send_message(recipient_id, 'Sure! On its way.')
                        send_message(recipient_id, 'Does this image contain a cat? https://tinyurl.com/ydanw4vz')
                    elif count == 1:
                        send_message(recipient_id, "Thanks! You've been credited $0.03.")
                    elif count == 2:
                        send_message(recipient_id, 'Sure! On its way.')
                        send_message(recipient_id, 'How positive is this article on a scale from 1 to 5? https://tinyurl.com/y8oppfmx')
                    elif count == 3:
                        send_message(recipient_id, "Thanks! You've been credited $0.04.")
                    elif count == 4:
                        send_message(recipient_id, 'Sure! On its way.')
                        send_message(recipient_id, 'Going forward, would you expect this graph to go up or down? https://tinyurl.com/y6ushjxv')
                    elif count == 5:
                        send_message(recipient_id, "Thanks! You've been credited $0.02.")

                    count += 1
                    """
                    try:
                        lines = message.get('message').get('text').split('\n')
                        people.username = lines[0][len('user:'):]
                        people.password = lines[1][len('pass:'):]
                        send_message(recipient_id, people.Query.get()['text'])
                    except Exception as e:
                        print(e)
                        send_message(recipient_id, 'Sorry, something must have gone wrong.')
                    """

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
