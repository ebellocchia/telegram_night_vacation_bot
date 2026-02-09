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
from typing import List

import pyrogram
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram_night_vacation_bot.bot_config import BotConfig
from telegram_night_vacation_bot.bot_msg import BotMessages
from telegram_night_vacation_bot.bot_type import BotTypes
from telegram_night_vacation_bot.telegram_client import TelegramClient
from telegram_night_vacation_bot.utils import Utils


class VacationNightConst:
    """Constants for vacation and night mode job scheduling."""

    NOTIFY_NIGHT_JOB_ID: str = "notify_night_job"
    NOTIFY_VACATION_JOB_ID: str = "notify_vacation_job"


class VacationNight:
    """Manages vacation and night mode functionality."""

    bot_type: BotTypes
    last_night_msg_ids: List[int]
    last_vacation_msg_ids: List[int]
    scheduler: AsyncIOScheduler
    tg_client: TelegramClient

    def __init__(
        self,
        bot_type: BotTypes,
        tg_client: TelegramClient
    ) -> None:
        """
        Initialize the vacation/night mode manager.

        Args:
            bot_type: The type of bot (TEST or NORMAL).
            tg_client: The Telegram client instance.
        """
        self.bot_type = bot_type
        self.tg_client = tg_client
        self.last_night_msg_ids = []
        self.last_vacation_msg_ids = []
        self.scheduler = AsyncIOScheduler()

    async def Init(self) -> None:
        """
        Initialize and start the scheduler.
        """
        self.scheduler.start()

    async def Start(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Start the vacation/night mode monitoring.

        Args:
            message: The message that triggered the start command.
        """
        try:
            self.scheduler.add_job(
                self.__NotifyNight,
                "cron",
                args=(BotConfig.CHAT_ID,),
                hour="*",
                id=VacationNightConst.NOTIFY_NIGHT_JOB_ID
            )
            self.scheduler.add_job(
                self.__NotifyVacation,
                "cron",
                args=(BotConfig.CHAT_ID,),
                hour=0,
                id=VacationNightConst.NOTIFY_VACATION_JOB_ID
            )
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_STARTED)
        except ConflictingIdError:
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_ALREADY_STARTED)

    async def Stop(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Stop the vacation/night mode monitoring.

        Args:
            message: The message that triggered the stop command.
        """
        try:
            self.scheduler.remove_job(VacationNightConst.NOTIFY_NIGHT_JOB_ID)
            self.scheduler.remove_job(VacationNightConst.NOTIFY_VACATION_JOB_ID)
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_STOPPED)
        except JobLookupError:
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_ALREADY_STOPPED)

    async def Status(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Check and report if the bot is running.

        Args:
            message: The message that triggered the status command.
        """
        if self.__IsRunning():
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_STATUS_RUNNING)
        else:
            await self.tg_client.SendMessageQuick(message, BotMessages.BOT_STATUS_STOPPED)

    async def NightStatus(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Check and report if night mode is active.

        Args:
            message: The message that triggered the night status command.
        """
        if self.__IsNight():
            await self.tg_client.SendMessageQuick(message, BotMessages.NIGHT_MODE_ACTIVE)
        else:
            await self.tg_client.SendMessageQuick(message, BotMessages.NIGHT_MODE_NOT_ACTIVE)

    async def VacationStatus(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Check and report if vacation mode is active.

        Args:
            message: The message that triggered the vacation status command.
        """
        if self.__IsVacationDay():
            await self.tg_client.SendMessageQuick(message, BotMessages.VACATION_MODE_ACTIVE)
        else:
            await self.tg_client.SendMessageQuick(message, BotMessages.VACATION_MODE_NOT_ACTIVE)

    async def TestVacation(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Test vacation mode notifications.

        Args:
            message: The message that triggered the test command.
        """
        await self.__NotifyVacation(BotConfig.CHAT_ID, True)

    async def TestNight(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Test night mode notifications.

        Args:
            message: The message that triggered the test command.
        """
        await self.__NotifyNight(BotConfig.CHAT_ID, True)

    async def OnMessage(
        self,
        message: pyrogram.types.Message
    ) -> None:
        """
        Handle incoming messages and delete if necessary.

        Args:
            message: The incoming message.
        """
        if not self.__IsRunning():
            return
        if not self.__IsNight() and not self.__IsVacationDay():
            return
        if not self.__IsUserValid(message):
            return

        chat_id = self.tg_client.GetChatIdFromMessage(message)
        topic_id = self.tg_client.GetTopicIdFromMessage(message)
        if self.__ShallMessageBeDeleted(chat_id, topic_id):
            user_id = self.tg_client.GetUserIdFromMessage(message)
            logging.info(f"Deleted message {message.id} from user: {user_id}, chat ID: {chat_id}, topic ID: {topic_id}")
            if not self.bot_type.IsTest():
                await self.tg_client.DeleteMessages(message.chat.id, [message.id])

    def __IsRunning(self) -> bool:
        """
        Check if the scheduler jobs are running.

        Returns:
            True if both jobs are running, False otherwise.
        """
        return (self.scheduler.get_job(VacationNightConst.NOTIFY_NIGHT_JOB_ID) is not None and
                self.scheduler.get_job(VacationNightConst.NOTIFY_VACATION_JOB_ID) is not None)

    def __IsUserValid(
        self,
        message: pyrogram.types.Message
    ) -> bool:
        """
        Check if the user should be subject to night/vacation mode.

        Args:
            message: The message to check.

        Returns:
            True if user is valid for deletion, False if excluded.
        """
        chat_id = self.tg_client.GetChatIdFromMessage(message)
        topic_id = self.tg_client.GetTopicIdFromMessage(message)

        if self.tg_client.IsUserAnonymous(message):
            logging.info(f"Anonymous user (chat ID: {chat_id}, topic ID: {topic_id}), skipped")
            return False
        if self.tg_client.IsUserBot(message):
            logging.info(f"Bot user (chat ID: {chat_id}, topic ID: {topic_id}), skipped")
            return False

        user = self.tg_client.GetUserFromMessage(message)
        user_id = self.tg_client.GetUserIdFromUser(user)
        username = self.tg_client.GetUsernameFromUser(user)
        if user_id in BotConfig.EXCLUDED_USERS or username in BotConfig.EXCLUDED_USERS:
            logging.info(f"Excluded user {user_id} (chat ID: {chat_id}, topic ID: {topic_id}), skipped")
            return False
        return True

    @staticmethod
    def __IsNight() -> bool:
        """
        Check if it's currently night time.

        Returns:
            True if current hour is within night hours, False otherwise.
        """
        hour = Utils.CurrentHour()
        return hour >= BotConfig.NIGHT_BEGIN_HOUR or hour < BotConfig.NIGHT_END_HOUR

    @staticmethod
    def __IsNightHour() -> bool:
        """
        Check if current hour is a night boundary hour.

        Returns:
            True if current hour is night begin or end hour, False otherwise.
        """
        hour = Utils.CurrentHour()
        return hour in [BotConfig.NIGHT_BEGIN_HOUR, BotConfig.NIGHT_END_HOUR]

    @staticmethod
    def __IsVacationDay() -> bool:
        """
        Check if today is a vacation day.

        Returns:
            True if today is a vacation day, False otherwise.
        """
        today = Utils.Today()
        if today.weekday() in BotConfig.VACATION_WEEK_DAYS:
            return True
        vacation_dates = BotConfig.VACATION_DATES
        if today.month in vacation_dates:
            return today.day in vacation_dates[today.month]
        return False

    @classmethod
    def __ShallMessageBeDeleted(
        cls,
        chat_id: int,
        topic_id: int
    ) -> bool:
        """
        Determine if a message should be deleted based on current mode.

        Args:
            chat_id: The chat ID.
            topic_id: The topic ID.

        Returns:
            True if message should be deleted, False otherwise.
        """
        if chat_id != BotConfig.CHAT_ID:
            return False
        if cls.__IsNight():
            return topic_id in BotConfig.NIGHT_TOPIC_IDS
        if cls.__IsVacationDay():
            return topic_id in BotConfig.VACATION_TOPIC_IDS
        return False

    async def __NotifyNight(
        self,
        chat_id: int,
        force: bool = False
    ) -> bool:
        """
        Send night mode notifications to configured topics.

        Args:
            chat_id: The chat ID to send notifications to.
            force: Force notification regardless of time.

        Returns:
            True if notification was sent, False otherwise.
        """
        if not force and not self.__IsNightHour():
            return False

        if len(self.last_night_msg_ids) > 0:
            logging.info(f"Deleted old night messages {self.last_night_msg_ids}")
            await self.tg_client.DeleteMessages(chat_id, self.last_night_msg_ids)
            self.last_night_msg_ids.clear()

        is_begin_hour = Utils.CurrentHour() == BotConfig.NIGHT_BEGIN_HOUR
        night_topic_ids = BotConfig.NIGHT_TOPIC_IDS
        for topic_id in night_topic_ids:
            if is_begin_hour:
                logging.info(f"Notified begin of night mode in topic {topic_id}")
                night_msg = BotMessages.NIGHT_BEGIN
            else:
                logging.info(f"Notified end of night mode in topic {topic_id}")
                night_msg = BotMessages.NIGHT_END

            sent_msgs = await self.tg_client.SendMessage(
                chat_id,
                topic_id,
                night_msg
            )
            self.last_night_msg_ids.extend([msg.id for msg in sent_msgs])
        return True

    async def __NotifyVacation(
        self,
        chat_id: int,
        force: bool = False
    ) -> bool:
        """
        Send vacation mode notifications to configured topics.

        Args:
            chat_id: The chat ID to send notifications to.
            force: Force notification regardless of vacation day.

        Returns:
            True if notification was sent, False otherwise.
        """
        if len(self.last_vacation_msg_ids) > 0:
            logging.info(f"Deleted old vacation messages {self.last_vacation_msg_ids}")
            await self.tg_client.DeleteMessages(chat_id, self.last_vacation_msg_ids)
            self.last_vacation_msg_ids.clear()

        if not force and not self.__IsVacationDay():
            return False

        vacation_topic_ids = BotConfig.VACATION_TOPIC_IDS
        for topic_id in vacation_topic_ids:
            logging.info(f"Notified vacation mode in topic {topic_id}")
            sent_msgs = await self.tg_client.SendMessage(
                chat_id,
                topic_id if topic_id > 0 else None,
                BotMessages.VACATION_DAY
            )
            self.last_vacation_msg_ids.extend([msg.id for msg in sent_msgs])
        return True
