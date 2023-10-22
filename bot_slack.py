import os
import random
import traceback
import datetime
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# read .env file
from dotenv import load_dotenv
load_dotenv()

# Update with your bot token
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# Update with the correct channel IDs
from_channel = os.environ["FROM_CHANNEL_ID"]
to_channel = os.environ["TO_CHANNEL_ID"]

logfile = "logbook.txt"

reactions = [
    "moyai",
    "smiling-imp",
    "face_with_monocle",
    "face_with_peeking_eye",
    "face_with_hand_over_mouth",
    "face_in_clouds",
    "skull",
]


def message_template(user, message):
    def n_space(n): return ' '*n
    return \
        f"""Never forget that once, *{user}* proudly declared:
        \n
```
{message}
{n_space(len(message))}— {user}
```
"""


def log_message(id):
    with open(logfile, "a") as f:
        f.write(f"{id}\n")


def get_logbook():
    with open(logfile, "r") as f:
        return f.read().splitlines()


def trim_logbook(percentage, logbook):
    trimmed_logbook = logbook[int(len(logbook) * percentage):]
    with open(logfile, "w") as f:
        f.write("\n".join(trimmed_logbook))
    return trimmed_logbook


def send_message(user, message, id):
    try:
        response = client.chat_postMessage(
            channel=to_channel,
            text=message_template(user=user, message=message),
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/%E5%90%B4%E5%8F%B8%E9%A9%AC%E5%AD%99%E6%AD%A6.jpg/220px-%E5%90%B4%E5%8F%B8%E9%A9%AC%E5%AD%99%E6%AD%A6.jpg",
            username="Quotes Bot"
        )
        client.reactions_add(
            channel=to_channel,
            timestamp=response.get("ts"),
            name=random.choice(reactions)
        )

        # log the message id to avoid sending it again in the future
        log_message(id)

    except SlackApiError as e:
        print("Error al send el message: ", e.response.get("error"))
    except:
        traceback.print_exc()


def is_quote(payload):
    try:
        if "files" in payload.keys():
            return False
        if "client_msg_id" not in payload.keys():
            return False
        text = payload.get("text")
        return text[0] == "\"" or text[0] == "\'"
    except:
        print(json.dumps(payload, indent=4))
        traceback.print_exc()
        return False


def chose_and_send_message():
    try:
        response = client.conversations_history(channel=from_channel)
        messages = list(filter(lambda x: is_quote(x),
                        response.get("messages")))
        if not messages:
            return

        already_chosen_messages = get_logbook()
        if len(already_chosen_messages) == len(messages):
            already_chosen_messages = trim_logbook(
                percentage=.3, logbook=already_chosen_messages)

        messages = list(filter(lambda x: x.get(
            "client_msg_id") not in already_chosen_messages, messages))

        chosen_msg = random.choice(messages)

        *msg_text, author = chosen_msg.get("text").split('"')
        msg_text = "".join(msg_text).strip()
        username = author.replace("-", "").strip().title()

        # send_message(user=username, message=msg_text, id=chosen_msg.get("client_msg_id"))

    except SlackApiError as e:
        print("Error al obtener los messages: ", e.response.get("error"))
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    if datetime.datetime.today().weekday() % 2 == 0:
        chose_and_send_message()
