# Copyright (c) 2026 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
from typing import Any, Callable, List, Optional

import pyrogram.types
from pyrogram import Client, idle
from pyrogram.types import ReplyParameters


class TelegramClientConst:
    """Constants used by the Telegram client."""

    ANONYMOUS_USERS_ID: int = -1
    MESSAGE_MAX_LEN: int = 4096
    TOPIC_NONE_ID: int = 0
    TOPIC_PRIVATE_ID: int = -1


class TelegramClient:
    """Wrapper for Telegram client to handle bot interactions."""

    client: Client

    def __init__(
        self,
        session_name: str,
        bot_token: str,
        api_id: str,
        api_hash: str
    ) -> None:
        """Initialize the Telegram client.

        Args:
            session_name: Name of the session file.
            bot_token: Bot token from BotFather.
            api_id: API ID from Telegram.
            api_hash: API hash from Telegram.
        """
        self.client = Client(
            session_name,
            bot_token=bot_token,
            api_id=api_id,
            api_hash=api_hash
        )

    @staticmethod
    def AnonymousUserId() -> int:
        """Get the ID used for anonymous users.

        Returns:
            int: The anonymous user ID constant.
        """
        return TelegramClientConst.ANONYMOUS_USERS_ID

    @staticmethod
    def TopicNoneId() -> int:
        """Get the ID representing no topic.

        Returns:
            int: The topic none ID constant.
        """
        return TelegramClientConst.TOPIC_NONE_ID

    def AddHandler(
        self,
        handler: Any
    ) -> None:
        """Add a message handler to the client.

        Args:
            handler: The handler to add.
        """
        self.client.add_handler(handler)

    async def Run(self) -> None:
        """Start the Telegram client."""
        async with self.client:
            await idle()

    async def SendMessage(
        self,
        chat_id: int,
        topic_id: Optional[int],
        message_text: str,
    ) -> List[pyrogram.types.Message]:
        """Send a message to a chat, splitting if necessary.

        Args:
            chat_id: The chat ID to send the message to.
            topic_id: The topic ID (optional).
            message_text: The message text to send.

        Returns:
            List of sent message objects.
        """
        sent_msgs = []
        split_text = self.__SplitMessageText(message_text)
        for text_part in split_text:
            msg = await self.client.send_message(
                chat_id,
                text_part,
                reply_parameters=ReplyParameters(message_id=topic_id or 0)
            )
            sent_msgs.append(msg)
        return sent_msgs

    async def SendMessageQuick(
        self,
        message: pyrogram.types.Message,
        message_text: str,
    ) -> List[pyrogram.types.Message]:
        """Send a message to the same chat as the original message.

        Args:
            message: The original message to extract chat and topic ID from.
            message_text: The message text to send.

        Returns:
            List of sent message objects.
        """
        return await self.SendMessage(
            self.GetChatIdFromMessage(message),
            self.GetTopicIdFromMessage(message),
            message_text
        )

    async def SendReplyMessage(
        self,
        original_message: pyrogram.types.Message,
        message_text: str
    ) -> List[pyrogram.types.Message]:
        """Send a reply to a message, splitting if necessary.

        Args:
            original_message: The message to reply to.
            message_text: The message text to send.

        Returns:
            List of sent message objects.
        """
        sent_msgs = []
        first = True
        split_text = self.__SplitMessageText(message_text)
        for text_part in split_text:
            if first:
                first = False
                msg = await self.client.send_message(
                    original_message.chat.id,
                    text_part,
                    reply_parameters=ReplyParameters(message_id=original_message.id)
                )
            else:
                msg = await self.client.send_message(original_message.chat.id, text_part)
            sent_msgs.append(msg)
        return sent_msgs

    async def DeleteMessages(
        self,
        chat_id: int,
        message_ids: List[int]
    ) -> None:
        """Delete messages from a chat.

        Args:
            chat_id: The chat ID.
            message_ids: List of message IDs to delete.
        """
        try:
            await self.client.delete_messages(chat_id, message_ids)
        except:
            pass

    async def Me(self) -> pyrogram.types.User:
        """Get the bot's user information.

        Returns:
            The bot's user object.
        """
        return await self.client.get_me()

    async def MyUsername(self) -> str:
        """Get the bot's username.

        Returns:
            The bot's username.
        """
        me = await self.Me()
        return me.username

    async def MentionedMe(
        self,
        message: pyrogram.types.Message
    ) -> bool:
        """Check if the bot was mentioned in a message.

        Args:
            message: The message to check.

        Returns:
            True if the bot was mentioned, False otherwise.
        """
        me = await self.Me()
        if me.username is None:
            return False
        return f"@{me.username.lower()}" in self.GetTextFromMessage(message).lower()

    async def RepliedToMe(
        self,
        message: pyrogram.types.Message
    ) -> bool:
        """Check if a message is a reply to the bot.

        Args:
            message: The message to check.

        Returns:
            True if the message is a reply to the bot, False otherwise.
        """
        me = await self.Me()
        replied = message.reply_to_message
        if replied is None:
            return False
        return replied.from_user is not None and replied.from_user.id == me.id

    @staticmethod
    def GetChatFromMessage(
        message: pyrogram.types.Message
    ) -> pyrogram.types.Chat:
        """Get the chat object from a message.

        Args:
            message: The message.

        Returns:
            The chat object.
        """
        return message.chat

    @staticmethod
    def GetChatIdFromMessage(
        message: pyrogram.types.Message
    ) -> int:
        """Get the chat ID from a message.

        Args:
            message: The message.

        Returns:
            The chat ID.
        """
        return message.chat.id

    @staticmethod
    def GetUserFromMessage(
        message: pyrogram.types.Message
    ) -> Optional[pyrogram.types.User]:
        """Get the user object from a message.

        Args:
            message: The message.

        Returns:
            The user object, or None if anonymous.
        """
        return message.from_user

    @classmethod
    def GetUserIdFromMessage(
        cls,
        message: pyrogram.types.Message
    ) -> int:
        """Get the user ID from a message.

        Args:
            message: The message.

        Returns:
            The user ID, or anonymous user ID if user is None.
        """
        user = cls.GetUserFromMessage(message)
        return cls.GetUserIdFromUser(user)

    @classmethod
    def IsUserAnonymous(
        cls,
        message: pyrogram.types.Message
    ) -> bool:
        """Check if the message sender is anonymous.

        Args:
            message: The message.

        Returns:
            True if the sender is anonymous, False otherwise.
        """
        return cls.GetUserFromMessage(message) is None

    @classmethod
    def IsUserBot(
        cls,
        message: pyrogram.types.Message
    ) -> bool:
        """Check if the message sender is a bot.

        Args:
            message: The message.

        Returns:
            True if the sender is a bot, False otherwise.
        """
        return not cls.IsUserAnonymous(message) and message.from_user.is_bot

    @staticmethod
    def IsPrivateChat(
            message: pyrogram.types.Message
    ) -> bool:
        """Check if the message is from a private chat.

        Args:
            message: The message.

        Returns:
            True if the chat is private, False otherwise.
        """
        if message.from_user is None:
            return False
        return message.from_user.id == message.chat.id

    @staticmethod
    def AppendTextInMessage(
        message: pyrogram.types.Message,
        text: str
    ) -> None:
        """Append text to a message's text or caption.

        Args:
            message: The message to modify.
            text: The text to append.
        """
        if message.text is not None:
            message.text += " " + text
        elif message.caption is not None:
            message.caption += " " + text

    @classmethod
    def AppendTextInMessageIfNotPresent(
        cls,
        message: pyrogram.types.Message,
        text: str
    ) -> None:
        """Append text to a message if the text is not already present.

        Args:
            message: The message to modify.
            text: The text to append.
        """
        if not re.search(re.escape(text), cls.GetTextFromMessage(message), re.IGNORECASE):
            cls.AppendTextInMessage(message, text)

    @staticmethod
    def ReplaceTextInMessage(
        message: pyrogram.types.Message,
        old_text: str,
        new_text: str
    ) -> None:
        """Replace text in a message's text or caption.

        Args:
            message: The message to modify.
            old_text: The text to replace.
            new_text: The replacement text.
        """
        if message.text is not None:
            message.text = re.sub(re.escape(old_text), new_text, message.text, flags=re.IGNORECASE)
        elif message.caption is not None:
            message.caption = re.sub(re.escape(old_text), new_text, message.caption, flags=re.IGNORECASE)

    @staticmethod
    def GetTextFromMessage(
        message: pyrogram.types.Message
    ) -> str:
        """Get the text content from a message.

        Args:
            message: The message.

        Returns:
            The message text or caption, or empty string if neither exists.
        """
        if message.text is not None:
            return message.text.strip()
        if message.caption is not None:
            return message.caption.strip()
        return ""

    @staticmethod
    def GetTopicIdFromMessage(
        message: pyrogram.types.Message
    ) -> int:
        """Get the topic ID from a message.

        Args:
            message: The message.

        Returns:
            The topic ID, or special constants for private/none.
        """
        if TelegramClient.IsPrivateChat(message):
            return TelegramClientConst.TOPIC_PRIVATE_ID

        if message.message_thread_id is not None:
            topic_id = message.message_thread_id
        else:
            topic_id = TelegramClientConst.TOPIC_NONE_ID
        return topic_id

    @classmethod
    def GetUserFullNameFromUser(
        cls,
        user: Optional[pyrogram.types.User]
    ) -> str:
        """Get the full name of a user.

        Args:
            user: The user object.

        Returns:
            The user's full name (first and last name combined).
        """
        if user is None:
            name = ""
        elif user.first_name is not None:
            name = f"{user.first_name} {user.last_name}" if user.last_name is not None else f"{user.first_name}"
        else:
            name = user.last_name if user.last_name is not None else ""
        return name

    @staticmethod
    def GetUserIdFromUser(
        user: Optional[pyrogram.types.User]
    ) -> int:
        """Get the ID from a user object.

        Args:
            user: The user object.

        Returns:
            The user ID, or anonymous user ID if user is None.
        """
        return user.id if user is not None else TelegramClientConst.ANONYMOUS_USERS_ID

    @staticmethod
    def GetUsernameFromUser(
        user: Optional[pyrogram.types.User]
    ) -> str:
        """Get the username from a user object.

        Args:
            user: The user object.

        Returns:
            The username, or empty string if user is None or has no username.
        """
        if user is None:
            return ""
        return user.username if user.username is not None else ""

    @staticmethod
    def GetCommandParameter(
        message: pyrogram.types.Message,
        index: int,
        default_val: Any,
        conv_fct: Callable[[str], Any] = str
    ) -> Any:
        """Get a command parameter from a message with type conversion.

        Args:
            message: The message containing the command.
            index: The parameter index.
            default_val: The default value if parameter is not found.
            conv_fct: Function to convert the parameter value.

        Returns:
            The converted parameter value, or default_val if not found.
        """
        try:
            return conv_fct(message.command[index])
        except (IndexError, ValueError):
            return default_val

    @staticmethod
    def __SplitMessageText(
        message_text: str
    ) -> List[str]:
        """Split a long message text into multiple parts respecting Telegram's limits.

        Args:
            message_text: The message text to split.

        Returns:
            List of message text parts.
        """
        msg_parts = []

        while len(message_text) > 0:
            # If length is less than maximum, the operation is completed
            if len(message_text) <= TelegramClientConst.MESSAGE_MAX_LEN:
                msg_parts.append(message_text)
                break

            # Take the current part
            curr_part = message_text[:TelegramClientConst.MESSAGE_MAX_LEN]
            # Get the last occurrence of a new line
            idx = curr_part.rfind("\n")

            # Split with respect to the found occurrence
            if idx != -1:
                msg_parts.append(curr_part[:idx])
                message_text = message_text[idx + 1:]
            else:
                msg_parts.append(curr_part)
                message_text = message_text[TelegramClientConst.MESSAGE_MAX_LEN + 1:]

        return msg_parts
