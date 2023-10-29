import os
import random
import logging
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

load_dotenv()

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# Update with the correct channel IDs
from_channel = os.environ["FROM_CHANNEL_ID"]
to_channel = os.environ["TO_CHANNEL_ID"]

LOGBOOK = "logbook.txt"

reactions = [
    "moyai",
    "smiling_imp",
    "face_with_monocle",
    "face_with_peeking_eye",
    "face_with_hand_over_mouth",
    "face_in_clouds",
    "skull",
]


def message_template(user, message):
    def n_space(n):
        return ' '*n
    return \
        f"""Never forget that once, *{user}* proudly declared:
        \n
```
{message}
{n_space(len(message))}— {user}
```
"""


def log_message(msg_id):
    with open(LOGBOOK, "a", encoding="utf-8") as f:
        f.write(f"{msg_id}\n")


def get_logbook():
    with open(LOGBOOK, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def trim_logbook(percentage, logbook):
    trimmed_logbook = logbook[int(len(logbook) * percentage):]
    with open(LOGBOOK, "w", encoding="utf-8") as f:
        f.write("\n".join(trimmed_logbook))
    return trimmed_logbook


def send_message(user, message, msg_id):
    try:
        response = client.chat_postMessage(
            channel=to_channel,
            text=message_template(user=user, message=message),
            icon_url="https://guidodinello.pythonanywhere.com/sun_tzu.jpg",
            username="Quotes Bot"
        )
        client.reactions_add(
            channel=to_channel,
            timestamp=response.get("ts"),
            name=random.choice(reactions)
        )

        # log the message id to avoid sending it again in the future
        log_message(msg_id)

    except SlackApiError:
        logging.exception("Error while sending message")


def is_quote(payload):
    try:
        # ignore not text messages
        if "files" in payload or "client_msg_id" not in payload:
            return False
        text = payload.get("text", "").strip()
        return text.startswith("\"") or text.startswith("\'")
    except Exception:  # pylint: disable=broad-except
        logging.exception(
            "Error while checking message: %s", json.dumps(payload, indent=4))
        return False


def chose_and_send_message():
    try:
        response = client.conversations_history(channel=from_channel)
        # filter out messages that are not quotes
        messages = list(filter(is_quote,
                        response.get("messages")))
        if not messages:
            return

        already_chosen_messages = get_logbook()
        if len(already_chosen_messages) == len(messages):
            already_chosen_messages = trim_logbook(
                percentage=.3, logbook=already_chosen_messages)

        # filter out already chosen messages
        messages = list(filter(lambda x: x.get(
            "client_msg_id") not in already_chosen_messages, messages))

        chosen_msg = random.choice(messages)

        *msg_text, author = chosen_msg.get("text").split('"')
        msg_text = "".join(msg_text).strip()
        username = author.replace("-", "").strip().title()

        send_message(user=username, message=msg_text,
                     msg_id=chosen_msg.get("client_msg_id"))

    except SlackApiError:
        logging.exception("Error while fetching messages")


if __name__ == "__main__":
    try:
        chose_and_send_message()
    except Exception:
        logging.exception("General Error")
        raise
