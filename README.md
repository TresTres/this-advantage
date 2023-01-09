# this-advantage

## Compend

### Setup
To setup compend-bot in an application, you'll need to do the following:
1. Create a new Discord application
2. Create a new bot underneath the application
3. Use the OAuth2 URL generator - select a _bot_ SCOPE and _Administrator_ PERMISSIONS
4. Use the generated URL to attach the bot to a server/guild 
5. Enable the `message_content` privileged intent for the bot
6. Generate and copy the bot token to the `COMPENT_DISCORD_TOKEN` env variable


### Local Run
Install the library by navigating to `this-advantage/compend` and running `poetry install`, then run the bot locally using `poetry run python bot.py`.

### Commands