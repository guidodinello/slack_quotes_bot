[![Code Quality Checks](https://github.com/guidodinello/slack_quotes_bot/actions/workflows/qa.yml/badge.svg?branch=main)](https://github.com/guidodinello/slack_quotes_bot/actions/workflows/qa.yml)

## Set up

Remember to update the three tokens in the .env file.

-   The slack token can be found in the slack api page, in the "OAuth & Permissions" section, under the "Bot User OAuth Token" label (only after the app is installed in the workspace).

-   The channel id is the last part of the url of the channel, can be found doing right click on the channel and then "Copy link".

Remember to add the bot to both channels.

## Scopes

The bot needs the following scopes:

-   group:history, View messages and other content in private channels that TestBot has been added to
-   chat:write, to Send messages as @TestBot
-   reactions:write, to add emoji reactions

## Hosting

Right now it runs a daily scheduled task on python-anywhere. Additionally you can checkout the github-hosted branch to get an idea of how to use a scheduled github action workflow to execute this bot. 
