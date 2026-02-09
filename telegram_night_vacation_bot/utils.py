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

import time
from datetime import datetime


class Utils:
    """Utility functions for date and time operations."""

    @staticmethod
    def Today() -> datetime:
        """
        Get the current date and time.

        Returns:
            datetime: The current datetime object.
        """
        return datetime.now()

    @staticmethod
    def CurrentDay() -> int:
        """
        Get the current day of the month.

        Returns:
            int: The current day (1-31).
        """
        return Utils.Today().day

    @staticmethod
    def CurrentHour() -> int:
        """
        Get the current hour of the day.

        Returns:
            int: The current hour (0-23).
        """
        return Utils.Today().hour

    @staticmethod
    def CurrentMonth() -> int:
        """
        Get the current month.

        Returns:
            int: The current month (1-12).
        """
        return Utils.Today().month

    @staticmethod
    def CurrentTime() -> float:
        """
        Get the current Unix timestamp.

        Returns:
            float: The current time in seconds since the epoch.
        """
        return time.time()
