VENV=SLACK_ENV
PY_VERSION="3.10"

python${PY_VERSION} -m venv "${VENV}"
# shellcheck source=./SLACK_ENV/bin/activate
. "./${VENV}/bin/activate"
pip3 install -r requirements.txt
# python${PY_VERSION} bot_slack.py