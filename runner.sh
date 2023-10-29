VENV="SLACK_ENV"
PY_VERSION="3.10"
SCRIPT="bot_slack.py"

git pull
if [ ! -d "${VENV}" ]; then
    echo "Creating virtual environment..."
    python${PY_VERSION} -m venv "${VENV}"
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate"
    pip3 install -r requirements.txt
else
    # shellcheck source=./SLACK_ENV/bin/activate
    . "./${VENV}/bin/activate"
fi
python${PY_VERSION} "${SCRIPT}"
