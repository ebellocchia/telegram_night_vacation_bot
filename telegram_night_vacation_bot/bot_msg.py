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


class BotMessages:
    """Constants for bot messages sent to users."""

    ALIVE: str = """🤖 Hello! 🤖
The bot is alive."""

    HELP: str = """🤖 Hello! 🤖
Commands for **night/vacation** control:

**/nvbot_help**: __show this message__
**/nvbot_alive**: __check if the bot is alive__
**/nvbot_start**: __start bot__
**/nvbot_stop**: __stop bot__
**/nvbot_status**: __show if bot is started or not__
**/nvbot_night_status**: __show if night mode is active or not__
**/nvbot_vacation_status**: __show if vacation mode is active or not__
**/nvbot_test_night**: __test the night mode notification in topics__
**/nvbot_test_vacation**: __test the vacation mode notification in topics__
**/nvbot_version**: __show the bot version__"""

    VERSION: str = """🤖 Hello! 🤖
Bot version: __{version}__"""

    USER_NOT_AUTHORIZED: str = "❌ You are not authorized to use the bot."

    BOT_STARTED: str = "✅ Bot started"
    BOT_ALREADY_STARTED: str = "❌ Bot already started"
    BOT_STOPPED: str = "✅ Bot stopped"
    BOT_ALREADY_STOPPED: str = "❌ Bot already stopped"
    BOT_STATUS_RUNNING: str = "🟢 Bot running"
    BOT_STATUS_STOPPED: str = "🔴 Bot stopped"

    NIGHT_MODE_ACTIVE: str = "🟢 Night mode active"
    NIGHT_MODE_NOT_ACTIVE: str = "🔴 Night mode inactive"
    VACATION_MODE_ACTIVE: str = "🟢 Vacation mode active"
    VACATION_MODE_NOT_ACTIVE: str = "🔴 Vacation mode inactive"

    NIGHT_BEGIN: str = """🌒 **NIGHT MODE**

Hello everyone,
Night mode has started. **You cannot** send messages in the group.

Thank you,
__The team__"""
    NIGHT_END: str = """🌒 **NIGHT MODE**

Hello everyone,
Night mode is over. **You can send messages in the group again.**

Thank you,
__The team__"""
    VACATION_DAY: str = """📝 **TOPIC CLOSED**

Hello everyone,
we would like to inform you that this topic will be closed today.

Thank you,
__The team__"""
