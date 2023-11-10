import os
import json
import argparse
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
channel_id = os.environ.get("TO_CHANNEL_ID")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a message from a channel")
    parser.add_argument(
        "--delete", nargs=1, type=str, help="The ts of the message you want to delete"
    )
    parser.add_argument(
        "--get_all", action="store_true", help="Get all messages from a channel"
    )
    args = parser.parse_args()

    if not slack_bot_token:
        slack_bot_token = input("SLACK_BOT_TOKEN:(example xoxb-...-...):")
    if not channel_id:
        channel_id = input("CHANNEL_ID (example C01B4PVGLVB):")

    client = WebClient(token=slack_bot_token)

    try:
        if args.delete:
            message_id = args.delete[0]
            # NOTE: client_msg_id used by bot_slack is not the same as ts
            result = client.chat_delete(channel=channel_id, ts=args.message_id)

        if args.get_all:
            response = client.conversations_history(channel=channel_id)
            with open("messages.json", "w", encoding="utf-8") as f:
                json.dump(response.data, f, indent=4)

    except SlackApiError as e:
        print(f"Error: {e}")
