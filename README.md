## Set up

Remember to update the three tokens in the .env file.
* The slack token can be found in the slack api page, in the "OAuth & Permissions" section, under the "Bot User OAuth Token" label (only after the app is installed in the workspace).

* The channel id is the last part of the url of the channel, can be found doing right click on the channel and then "Copy link".

Rememer to add the bot to both channels.

## Scopes

The bot needs the following scopes:
* group:history, View messages and other content in private channels that TestBot has been added to
* chat:write, to Send messages as @TestBot
* users:read, View people in a workspace (usernames)

## Do i need to have the script running all the time?

You need to have the script running continuously in order to maintain the scheduled functionality. The BlockingScheduler from the apscheduler library will run your elegir_y_enviar_mensaje function at the specified interval (in this case, every day) as long as the script is running.

In other words, you'll need to keep the script running in the background to ensure that your bot continues to execute the task of selecting and sending messages on the specified schedule.

If you close the script or terminate its execution, the scheduled task will stop. If you want to automate this process without having to keep the script running on your local machine, you could consider deploying your script to a server or a cloud environment where it can run continuously. This way, you won't have to worry about keeping your local machine turned on and the script running all the time.

Some options for deploying your script include:

* Cloud-based platforms like AWS, Google Cloud, or Azure.
* Hosting services like Heroku or PythonAnywhere.
* Dedicated servers or virtual private servers (VPS).

By deploying your script, you ensure that the scheduled task continues to run even if your local machine is turned off or the script process is stopped.

## Hosting
Right now it runs a daily scheduled task on python-anywhere
