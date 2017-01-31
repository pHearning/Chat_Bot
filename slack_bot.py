import time
import datetime
from slackclient import SlackClient
 
BOT_TOKEN = "<TOKEN>"
CHANNEL_ID = "C3XF3Q285"
USER_ID = "U3YUCC5AN"
 
def send_message(sc, message):
    sc.api_call("chat.postMessage", channel=CHANNEL_ID, text=message, username="ted_chat")

def bot_reaction(sc, message, user):
    """
    The function that you need to change to do what you want.
    Keyword arguments:
    sc -- the slack client instance that you use to make the API calls
    message -- the message that was sent
    user -- the user that sent the message
    """
    send_message(sc, "I'm alive!!!")

def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)
 
    # Connect to slack
    if sc.rtm_connect():
        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                if user != USER_ID: # The bot only reacts to messages that are not coming from itself
                    bot_reaction(sc, message, user)
            # Sleep for half a second
            time.sleep(0.5)

if __name__ == '__main__':
    main()
