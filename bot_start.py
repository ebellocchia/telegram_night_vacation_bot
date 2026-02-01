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

#
# Imports
#
import asyncio
import sys

from telegram_night_vacation_bot import Bot, BotTypes, __version__


#
# Functions
#

# Print header
def print_header() -> None:
    """Print the bot header with version information."""
    print("")
    print("***************************************")
    print("****                               ****")
    print("***                                 ***")
    print("**                                   **")
    print("*     Telegram Vacation/Night Bot     *")
    print("*     Author: Emanuele Bellocchia     *")
    print(f"*           Version: {__version__}            *")
    print("**                                   **")
    print("***                                 ***")
    print("****                               ****")
    print("***************************************")
    print("")


async def main() -> None:
    """Main async entry point for the bot."""
    bot_type = BotTypes(int(sys.argv[1])) if len(sys.argv) > 1 else BotTypes.TEST
    bot = Bot(bot_type)
    await bot.Init()
    await bot.Run()


if __name__ == "__main__":
    # Print header
    print_header()
    # Run async main
    asyncio.run(main())
