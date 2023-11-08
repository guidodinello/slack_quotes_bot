#!/bin/bash

VENV="SLACK_ENV"
SCRIPT="bot_slack.py"

git pull
if [ ! -d "${VENV}" ]; then
    echo "Creating virtual environment..."
    python -m venv "${VENV}" || (echo "Failed to create virtual environment" && exit 1)
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate" || (echo "Failed to activate virtual environment" && exit 1)
    pip3 install -r requirements.txt
else
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate"
fi
python "${SCRIPT}"
