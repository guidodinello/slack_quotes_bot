#!/bin/bash

VENV="SLACK_ENV"
PY_VERSION="3.12"
SCRIPT="bot_slack.py"

git pull
if [ ! -d "${VENV}" ]; then
    echo "Creating virtual environment..."
    python${PY_VERSION} -m venv "${VENV}" || (echo "Failed to create virtual environment" && exit 1)
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate" || (echo "Failed to activate virtual environment" && exit 1)
    pip3 install -r requirements.txt
else
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate"
fi
python${PY_VERSION} "${SCRIPT}"
