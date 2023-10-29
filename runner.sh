#!/bin/sh

git pull
. SLACK_ENV/bin/activate
python3.10 bot_slack.py