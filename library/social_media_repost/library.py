"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout

from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback

from assets.telegram.api import post_message
from assets.twitter.api import tweet

from .filters import NewPost
from .templates import (
    TELEGRAM_CHANNEL_NOTIFICATION,
    SUCCESS_REPOST,
    EXCEPTION_MESSAGE
)


class Reposter(Library):
    """
    Lib that reposts new post to X and Telegram
    """

    @callback(NewPost)
    async def repost(self, toolkit, package):
        """
        Repost handler
        """

        tweet_result = SUCCESS_REPOST
        result_type = LogLevel.DEBUG

        post_id = f"wall{package.owner_id}_{package.id}"
        post_link = f"https://vk.com/{post_id}"
        notification = TELEGRAM_CHANNEL_NOTIFICATION.format(post_link=post_link)

        try:
            await tweet(toolkit, package.text, package.attachments)
            await post_message(notification)

        except ReadTimeout as exception:
            tweet_result = EXCEPTION_MESSAGE.format(exception=exception)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.messages.send(package, tweet_result)