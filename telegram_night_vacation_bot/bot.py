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

from telegram_night_vacation_bot.bot_config import BotConfig
from telegram_night_vacation_bot.bot_type import BotTypes
from telegram_night_vacation_bot.commands_night_vacation import CommandsNightVacation
from telegram_night_vacation_bot.logger import Logger
from telegram_night_vacation_bot.telegram_client import TelegramClient


class Bot:
    """Main bot class that manages the Telegram bot and its commands."""

    commands_nv: CommandsNightVacation
    tg_client: TelegramClient

    def __init__(
        self,
        bot_type: BotTypes
    ) -> None:
        """Initialize the bot with the specified type.

        Args:
            bot_type: The type of bot (TEST or NORMAL).
        """
        tg_client = TelegramClient(
            BotConfig.SESSION_NAME,
            BotConfig.BOT_TOKEN,
            BotConfig.API_ID,
            BotConfig.API_HASH
        )
        Logger.Init()

        self.commands_nv = CommandsNightVacation(bot_type, tg_client)
        self.tg_client = tg_client
        self.__LogConfig(bot_type)

    async def Run(self) -> None:
        """Start running the bot."""
        logging.info("Bot running")
        await self.tg_client.Run()

    async def Init(self) -> None:
        """Initialize bot commands."""
        await self.commands_nv.Init()

    @staticmethod
    def __LogConfig(
        bot_type: BotTypes
    ) -> None:
        """Log the bot configuration.

        Args:
            bot_type: The type of bot being configured.
        """
        logging.info("***** CONFIGURATION *****")
        logging.info(f"Bot type: {bot_type.name}")
        logging.info(f"Bot token: {BotConfig.BOT_TOKEN}")
        logging.info(f"Session name: {BotConfig.SESSION_NAME}")
        logging.info(f"Night begin hour: {BotConfig.NIGHT_BEGIN_HOUR}")
        logging.info(f"Night end hour: {BotConfig.NIGHT_END_HOUR}")
        logging.info(f"Vacation week days: {BotConfig.VACATION_WEEK_DAYS}")
        logging.info(f"Vacation dates: {BotConfig.VACATION_DATES}")
        logging.info(f"Night topic IDs: {BotConfig.NIGHT_TOPIC_IDS}")
        logging.info(f"Vacation topic IDs: {BotConfig.VACATION_TOPIC_IDS}")
        logging.info(f"Authorized users: {BotConfig.AUTHORIZED_USERS}")
        logging.info(f"Excluded users: {BotConfig.EXCLUDED_USERS}")
