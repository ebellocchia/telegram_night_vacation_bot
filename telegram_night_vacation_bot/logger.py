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


class Logger:
    """Logger configuration utility for the bot."""

    @staticmethod
    def Init() -> None:
        """Initialize the logging system based on bot configuration."""
        if not BotConfig.LOG_USE_FILE:
            logging.basicConfig(
                level=BotConfig.LOG_LEVEL,
                format="%(asctime)-15s %(levelname)s - %(message)s"
            )
        else:
            logging.basicConfig(
                level=BotConfig.LOG_LEVEL,
                filename=BotConfig.LOG_FILE_NAME,
                format="%(asctime)-15s %(levelname)s - %(message)s"
            )
