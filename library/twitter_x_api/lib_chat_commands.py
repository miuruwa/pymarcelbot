"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library

from vkbotkit.objects.enums import LogLevel

from .api import tweet
from .templates import RIGHTS_ERROR, NO_MESSAGE, NO_ERRORS, EXCEPTION_MESSAGE
from .filters import NotAdmin, TweetTrouble, MessageToTweet


class ChatCommands(Library):
    """
    Chat commands
    """

    @callback(NotAdmin)
    async def taboo(self, toolkit, package):
        await toolkit.messages.send(package, RIGHTS_ERROR)


    @callback(TweetTrouble)
    async def tweet_help(self, toolkit, package):
        """
        Send help message to user
        """
        
        bot_mention = await toolkit.get_my_mention()

        await toolkit.messages.send(package, NO_MESSAGE.format(bot_mention = repr(bot_mention)))
    

    @callback(MessageToTweet)
    async def tweet(self, toolkit, package):
        message_to_tweet = " ".join(package.items[2:])
        tweet_result = NO_ERRORS
        result_type = LogLevel.DEBUG

        try:
            await tweet(toolkit, message_to_tweet, package.attachments)

        except Exception as e:
            tweet_result = EXCEPTION_MESSAGE.format(exception=e)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.messages.send(package, tweet_result)