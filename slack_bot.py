import time
import datetime
from slackclient import SlackClient
 
BOT_TOKEN = "<TOKEN>"
CHANNEL_NAME = "general"
 
def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)
 
    # Connect to slack
    if sc.rtm_connect():
        # Send first message
        # sc.api_call("chat.postMessage",channel="C3XF3Q285",text="I'm ALIVE!!",username="ted_chat")        
 
        while True:
            # print(sc.api_call("channels.replies",channel="C3XF3Q285", thread_ts=time.time()))
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                if user != 'U3YUCC5AN':
                    sc.api_call("chat.postMessage",
                                channel="C3XF3Q285",
                                text="I'm ALIVE!!",
                                username="ted_chat")
            # Sleep for half a second
            time.sleep(0.5)

if __name__ == '__main__':
    main()
