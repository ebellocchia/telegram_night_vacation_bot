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
from typing import Dict, List, Union


class BotConfig:
    """Configuration settings for the bot."""

    # API ID/Hash from https://my.telegram.org/apps
    API_ID: str = "0000000"
    API_HASH: str = "00000000000000000000000000000000"
    # Bot token from BotFather
    BOT_TOKEN: str = "0000000000:AAAAAAAAAAAA-0000000000000000000000"
    # Name of session file
    SESSION_NAME: str = "data/session/tg_bot_nv_session"

    # Log level
    LOG_LEVEL: int = logging.INFO
    # If False, logs will be written to console
    # If True, logs will be written to file
    LOG_USE_FILE: bool = False
    # Only used if LOG_USE_FILE is True
    LOG_FILE_NAME: str = "data/logs/tg_bot_nv_log.txt"

    # Night begin hour (e.g. 22 -> 22:00)
    NIGHT_BEGIN_HOUR: int = 22
    # Night end hour (e.g. 8 -> 8:00)
    NIGHT_END_HOUR: int = 8
    # List of days of the week considered "vacation" (0: Monday, 1: Tuesday, 2: Wednesday, ..., 6: Sunday)
    # For example:
    #   Vacation days = [1, 6] -> The topics will be closed every Monday and Sunday
    VACATION_WEEK_DAYS: List[int] = [6]

    #
    # Vacation dates
    # Format:
    #   month: [day_1, day_2, ...]
    #
    # For example:
    #   1: [1, 6]  -> 1st January, 6th January
    #   5: [1]     -> 1st May
    #
    VACATION_DATES: Dict[int, List[int]] = {
        1: [1, 6],
        5: [1],
        8: [15],
        11: [1],
        12: [8, 25, 26],
    }

    # ID of the group
    # Use test mode to get the topic IDs (every message is logged)
    CHAT_ID: int = -1000000000000
    # List of topics that are closed during the night
    # Use test mode to get the topic IDs (every message is logged)
    NIGHT_TOPIC_IDS: List[int] = [0, 1]
    # List of topics that are closed during vacation
    # Use test mode to get the topic IDs (every message is logged)
    VACATION_TOPIC_IDS: List[int] = [1]

    # List of users that are authorized to use the bot
    # The list can contain both user IDs and usernames (without the '@')
    AUTHORIZED_USERS: List[Union[int, str]] = [
        000000000,
        "username",
    ]
    # List of users that are excluded from night/vacation mode, i.e. can still write during night or vacation
    # The list can contain both user IDs and usernames (without the '@')
    EXCLUDED_USERS: List[Union[int, str]] = [
        000000000,
        "username",
    ]
