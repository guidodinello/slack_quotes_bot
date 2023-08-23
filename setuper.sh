VENV=SLACK_ENV


python3 -m venv $VENV
source ${VENV}/bin/activate
pip3 install -r requirements.txt
python3 bot_slack.py