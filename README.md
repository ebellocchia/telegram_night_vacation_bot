# Telegram Night Vacation Bot

[![Code Analysis](https://github.com/ebellocchia/telegram_night_vacation_bot/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/ebellocchia/telegram_night_vacation_bot/actions/workflows/code-analysis.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/ebellocchia/telegram_night_vacation_bot/badge)](https://www.codefactor.io/repository/github/ebellocchia/telegram_night_vacation_bot)
[![GitHub License](https://img.shields.io/github/license/ebellocchia/telegram_night_vacation_bot?label=License)](https://github.com/ebellocchia/telegram_night_vacation_bot?tab=MIT-1-ov-file)

## Introduction

Telegram bot for managing night and vacation modes in groups based on *pyrogram*.\
During night or vacation days (both configurable), the bot automatically deletes every message sent in the chat.

The bot supports topics: it can activate night or vacation mode in all or only some topics (it also works with no topics, of course).\
The beginning and end of night are notified with a message in every topic, at the configured hours.\
The beginning of vacation is notified with a message in every topic at midnight.

When a new notification message is sent, the old one is deleted to avoid polluting the chat.

## Setup

### Create Telegram app

In order to use the bot, in addition to the bot token you also need an API ID and hash.\
To get them, create an app using the following website: [https://my.telegram.org/apps](https://my.telegram.org/apps).

### Usage

This package requires **Python >= 3.7**.


1. **Set up a virtual environment (optional but recommended)**:

```
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

2. **Install the requirements:**

```
pip install -r requirements.txt
```

**IMPORTANT NOTE:** This bot uses *pyrotgfork*. If you are not using a virtual environment, ensure that the standard *pyrogram* library (or forks) is not installed in your Python environment.
Since both libraries use the same package name, having both installed will cause conflicts and the bot will not function correctly.

3. **Set up the bot:**
Edit the configuration class by specifying your API ID, API hash, bot token, and other parameters according to your needs (see the "Configuration" chapter).
4. **Run the bot:**
Launch the **bot_start.py** script to start the bot.
Pass `0` as an argument to start the bot in test mode (default), `1` to start it in production mode.

```
python bot_start.py    # Test mode

python bot_start.py 0  # Test mode

python bot_start.py 1  # Production mode
```

## Configuration

To configure the bot, just edit the `BotConfig` class (`telegram_night_vacation_bot.bot_config.py`).\
The list of all possible configuration elements is shown below.

|Name| Description |
|---|---|
|`API_ID`|API ID from [https://my.telegram.org/apps](https://my.telegram.org/apps).|
|`API_HASH`|API hash from [https://my.telegram.org/apps](https://my.telegram.org/apps).|
|`BOT_TOKEN`|Bot token from *BotFather*.|
|`SESSION_NAME`|Path of the file used to store the session.|
|`LOG_LEVEL`|Log level, same of python logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)|
|`LOG_USE_FILE`|If true, logs will be written to a file, if false they'll be written to the console.|
|`LOG_FILE_NAME`|Log file name (only if `LOG_USE_FILE` is True).|
|`NIGHT_BEGIN_HOUR`|Night begin hour, integer value (e.g. __22 -> 22:00__).|
|`NIGHT_END_HOUR`|Night end hour, integer value (e.g. __8 -> 8:00__).|
|`VACATION_WEEK_DAYS`|List of days of the week considered "vacation" (__0: Monday, 1: Tuesday, 2: Wednesday, ..., 6: Sunday__).|
|`VACATION_DATES`|List of dates considered "vacation". The list of days is specified for a month (format: __month: [day_1, day_2, ...]__).|
|`CHAT_ID`|ID of the group. Run the bot in test mode to get the topic IDs.|
|`NIGHT_TOPIC_IDS`|IDs of the topics where the night mode is activated. Run the bot in test mode to get the topic IDs.|
|`VACATION_TOPIC_IDS`|IDs of the topics where the vacation mode is activated. Run the bot in test mode to get the topic IDs.|
|`AUTHORIZED_USERS`|List of users that are authorized to use the bot (user IDs and/or usernames).|
|`EXCLUDED_USERS`|List of users that are excluded from night/vacation mode, i.e. who can still write during night or vacation (user IDs and/or usernames).|

If the group has no topics, there will be only one topic with ID `0`.

Every configuration element is documented inside the class.

## Supported Commands

List of supported commands:
- `vnbot_help`: show the list of supported commands
- `vnbot_alive`: show if bot is alive
- `nvbot_start`: start the bot (i.e. start notifying night and vacation, deleting messages during night and vacation)
- `nvbot_stop`: stop the bot (i.e. stop notifying night and vacation, deleting messages during night and vacation)
- `nvbot_status`: show if bot is currently started or not
- `nvbot_night_status`: show if night mode is currently active (it's shown regardless of whether the bot is started or not)
- `nvbot_vacation_status`: show if vacation mode is currently active (it's shown regardless of whether the bot is started or not)
- `nvbot_test_night`: send the night notification in topics (for testing)
- `nvbot_test_vacation`: send the vacation notification in topics (for testing)
- `nvbot_version`: show the bot version

The bot can only manage a single group (i.e. `BotConfig.CHAT_ID`).

## Translation

All the messages sent by the bot are defined inside the `BotMessages` class (`telegram_night_vacation_bot.bot_msg.py`).\
So, if you need to modify or translate the messages, just edit the strings inside the class.

## Run the Bot

It'd be better if the bot is an administrator of the group. This is mandatory if it needs to delete previously sent messages.\
In order to manage night and vacation modes, the bot should run 24/7. So, it's suggested to run it on a VPS (there is no performance requirements, so a cheap VPS will suffice).

Docker files are also provided, to run the bot in a Docker container:

```
docker compose up -d --build
```

**NOTE:** Depending on your timezone, you may want to adjust the `TZ=Europe/Rome` variable in `docker-compose.yml`.

## Test Mode

During test mode, the bot will work as usual but the messages won't be deleted (only a message will be logged to notify the deletion).\
Moreover, every sent message will be logged, allowing you to identify the chat and topic IDs.

# License

This software is available under the MIT license.
