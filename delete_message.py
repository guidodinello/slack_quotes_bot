import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", input(
    "SLACK_BOT_TOKEN:(example xoxb-...-...):"))
channel_id = os.environ.get("TO_CHANNEL_ID", input(
    "CHANNEL_ID (example C01B4PVGLVB):"))

# The ts of the message you want to delete (see logs file)
message_id = input("MESSAGE_ID (example 1698547167.668069):")


client = WebClient(token=slack_bot_token)

try:
    # Call the chat.chatDelete method using the built-in WebClient
    result = client.chat_delete(
        channel=channel_id,
        ts=message_id
    )

except SlackApiError as e:
    print(f"Error deleting message: {e}")
