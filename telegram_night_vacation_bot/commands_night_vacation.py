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

import logging

import pyrogram
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from telegram_night_vacation_bot._version import __version__
from telegram_night_vacation_bot.bot_config import BotConfig
from telegram_night_vacation_bot.bot_msg import BotMessages
from telegram_night_vacation_bot.bot_type import BotTypes
from telegram_night_vacation_bot.telegram_client import TelegramClient
from telegram_night_vacation_bot.vacation_night import VacationNight


class CommandsNightVacation:
    """Handler for night/vacation bot commands."""

    bot_type: BotTypes
    tg_client: TelegramClient
    night_vacation: VacationNight

    def __init__(
        self,
        bot_type: BotTypes,
        tg_client: TelegramClient
    ) -> None:
        """
        Initialize the commands handler.

        Args:
            bot_type: The type of bot (TEST or NORMAL).
            tg_client: The Telegram client instance.
        """
        self.bot_type = bot_type
        self.tg_client = tg_client
        self.night_vacation = VacationNight(bot_type, tg_client)

    async def Init(self) -> None:
        """Initialize and register all command handlers."""
        await self.night_vacation.Init()
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandHelp, filters.command(["start"]) & filters.private)
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandHelp, filters.command(["nvbot_help"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandAlive, filters.command(["nvbot_alive"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandStart, filters.command(["nvbot_start"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandStop, filters.command(["nvbot_stop"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandStatus, filters.command(["nvbot_status"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandVacationStatus, filters.command(["nvbot_vacation_status"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandNightStatus, filters.command(["nvbot_night_status"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandTestVacation, filters.command(["nvbot_test_vacation"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandTestNight, filters.command(["nvbot_test_night"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__CommandVersion, filters.command(["nvbot_version"]))
        )
        self.tg_client.AddHandler(
            MessageHandler(self.__OnMessage, filters.group)
        )
        logging.info("Commands initialized")

    async def __CommandHelp(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the help command to show available commands.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: help")
        await self.tg_client.SendMessageQuick(message, BotMessages.HELP)

    async def __CommandAlive(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the alive command to check if bot is responsive.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: alive")
        await self.tg_client.SendReplyMessage(message, BotMessages.ALIVE)

    async def __CommandVersion(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the version command to show bot version.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: version")
        await self.tg_client.SendMessageQuick(message, BotMessages.VERSION.format(version=__version__))

    async def __CommandStart(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the start command to activate the bot.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: start")
        await self.night_vacation.Start(message)

    async def __CommandStop(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the stop command to deactivate the bot.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: stop")
        await self.night_vacation.Stop(message)

    async def __CommandStatus(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the status command to show bot running status.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: status")
        await self.night_vacation.Status(message)

    async def __CommandVacationStatus(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the vacation status command to check if vacation mode is active.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: vacation status")
        await self.night_vacation.VacationStatus(message)

    async def __CommandNightStatus(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the night status command to check if night mode is active.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: night status")
        await self.night_vacation.NightStatus(message)

    async def __CommandTestVacation(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the test vacation command to test vacation notifications.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: night vacation")
        await self.night_vacation.TestVacation(message)

    async def __CommandTestNight(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle the test night command to test night notifications.

        Args:
            client: The Pyrogram client instance.
            message: The message that triggered the command.
        """
        if not await self.__IsUserAuthorized(message):
            return
        logging.info("Command: night test")
        await self.night_vacation.TestNight(message)

    async def __OnMessage(
        self,
        client: pyrogram.Client,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle incoming group messages.

        Args:
            client: The Pyrogram client instance.
            message: The incoming message.
        """
        self.__LogMessage(message)
        await self.night_vacation.OnMessage(message)

    async def __IsUserAuthorized(
        self,
        message: pyrogram.types.Message
    ) -> bool:
        """
        Check if the user is authorized to use the bot.

        Args:
            message: The message to check authorization for.

        Returns:
            True if user is authorized, False otherwise.
        """
        user = self.tg_client.GetUserFromMessage(message)
        user_id = self.tg_client.GetUserIdFromUser(user)
        username = self.tg_client.GetUsernameFromUser(user)
        if user_id in BotConfig.AUTHORIZED_USERS or username in BotConfig.AUTHORIZED_USERS:
            return True

        await self.tg_client.SendMessageQuick(message, BotMessages.USER_NOT_AUTHORIZED)
        return False

    def __LogMessage(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Log message details in test mode.

        Args:
            message: The message to log.
        """
        if self.bot_type.IsProduction():
            return

        chat_id = self.tg_client.GetChatIdFromMessage(message)
        topic_id = self.tg_client.GetTopicIdFromMessage(message)
        user = self.tg_client.GetUserFromMessage(message)
        user_full_name = self.tg_client.GetUserFullNameFromUser(user)
        user_id = self.tg_client.GetUserIdFromUser(user)
        username = self.tg_client.GetUsernameFromUser(user)

        logging.info(
            f"Got message from user: {user_full_name} (@{username}), user ID: {user_id}, chat ID: {chat_id}, topic ID: {topic_id}"
        )
