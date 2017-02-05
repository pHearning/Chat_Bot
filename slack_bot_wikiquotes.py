import time
import datetime
import wikiquote
from slackclient import SlackClient

BOT_TOKEN = "<TOKEN>"
CHANNEL_ID = "C3XF3Q285"
USER_ID = "U3YUCC5AN"


class QuoteMaster():
    rand = ""

    def send_message(self, sc, message):
        sc.api_call("chat.meMessage", channel=CHANNEL_ID, text=message, username="ted_chat")

    def search(self, sc, message):
        search = wikiquote.search(message)
        if search:
            quotes = wikiquote.quotes(search[0], max_quotes=1)
            for quote in quotes:
                self.send_message(sc, search[0] + ": " + quote)
        else:
            self.send_message(sc, "That's not a thing")

    def quoteMe(self, sc):

        self.rand = wikiquote.random_titles(max_titles=1)[0]
        quotes = wikiquote.quotes(self.rand, max_quotes=1)
        message = ""
        for quote in quotes:
            if len(quote) < 80:
                message = quote
        if message:
            self.send_message(sc, message + ", Who am I?")
        else:
            self.send_message(sc, quotes[0] + ", Who am I?")

    def answer(self, sc, message):
        correct_words = []
        answer = message.lower().split(" ")
        print(self.rand)
        for word in self.rand.split(" "):
            if word.lower() in answer:
                print(answer)
                print(word)
                correct_words.append(word)

        if correct_words:
            self.send_message(sc, ", ".join(correct_words) + " is correct")
        else:
            self.send_message(sc, "Wrong, you are wrong!")

    def tellMeMore(self, sc, message):
        search = wikiquote.search(message)
        if search:
            quotes = wikiquote.quotes(search[0], max_quotes=10000)
            for quote in quotes:
                if message.lower() in quote.lower():
                    self.send_message(sc, search[0] + ": " + quote)
        else:
            self.send_message(sc, "That's not a thing")

    def bot_reaction(self, sc, message, user):
        """
        The function that you need to change to do what you want.
        Keyword arguments:
        sc -- the slack client instance that you use to make the API calls
        message -- the message that was sent
        user -- the user that sent the message
        """
        if message.lower().startswith("search"):
            self.search(sc, message[8:])
        elif message.lower().startswith("tell me"):
            self.tellMeMore(sc, message[9:])
        elif message.lower().startswith("quote me"):
            self.quoteMe(sc)
        elif message.lower().startswith("answer"):
            self.answer(sc, message[7:])


def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)
    quoteBot = QuoteMaster()

    # Connect to slack
    if sc.rtm_connect():
        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                if user != USER_ID:  # The bot only reacts to messages that are not coming from itself
                    quoteBot.bot_reaction(sc, message, user)
            # Sleep for half a second
            time.sleep(0.5)


if __name__ == '__main__':
    main()
