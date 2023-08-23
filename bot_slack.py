import os
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.blocking import BlockingScheduler

# read .env file
from dotenv import load_dotenv
load_dotenv()

# Update with your bot token
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# Update with the correct channel IDs
from_channel = os.environ["FROM_CHANNEL_ID"]
to_channel = os.environ["TO_CHANNEL_ID"]

emojis = {
    "face-with-hand-over-mouth" : "🤭",
    "face-with-tears-of-joy" : "😂",
    "dizzy" : "💫",
    "sparkles" : "✨"
}

def message_template(user, mensaje):
    n_ident = lambda n: '\t'*n
    n_emoji = lambda n, emoji: (emojis[emoji] + " ")*n
    return \
f"""{emojis['sparkles']}Daily reminder that {emojis['sparkles']}:  
\t"{mensaje}"
{n_ident(20)}— {user} {emojis['face-with-hand-over-mouth']}{emojis['face-with-tears-of-joy']}
"""

def enviar_mensaje(user, mensaje):
    try:
        response = client.chat_postMessage(
            channel=to_channel,
            text=message_template(user=user, mensaje=mensaje)
        )
        print("Mensaje enviado: ", response.get("message").get("text"))
    except SlackApiError as e:
        print("Error al enviar el mensaje: ", e.response.get("error"))

def elegir_y_enviar_mensaje():
    try:
        response = client.conversations_history(channel=from_channel)
        mensajes = list(filter(lambda x: "client_msg_id" in x.keys(), response.get("messages")))
        mensaje_elegido = random.choice(mensajes)
        
        user_id = mensaje_elegido.get("user")
        user_info = client.users_info(user=user_id)
        username = user_info.get("user").get("name")
        
        enviar_mensaje(user=username, mensaje=mensaje_elegido.get("text"))
    except SlackApiError as e:
        print("Error al obtener los mensajes: ", e.response.get("error"))

# scheduler = BlockingScheduler()
# scheduler.add_job(elegir_y_enviar_mensaje, "interval", days=1)
# scheduler.start()

# For testing, manually trigger the message sending
elegir_y_enviar_mensaje()
