
# Compend

## Setup

Compend bot requires communciation with Discord and Notion APIs:
1. Set up a Notion integration and ensure that it has access to the pages you wish to include
2. Set up a Discord application and bot with the correct permissions and add it to a guild

## Discord Specifics 
To setup compend-bot in an application, you'll need to do the following on the Discord developer website:
1. Create a new Discord application
2. Create a new bot under the application
3. Use the OAuth2 URL generator - select a _bot_ and _application.commands_ SCOPE 
4. Enable the `message_content` privileged intent for the bot
5. Generate and copy the bot token to the `COMPEND_DISCORD_TOKEN` env variable

Then you'll need to do the following in the Disord app:
1. Use the generated URL to attach the bot to a server/guild 
2. Then you need to set up some base permissions;
   1. First, I recommend creating a non-admin role for users, so that you can use it to view the guild.  This will allow you to test the visibility of the bot and its commands without getting tricked by your guild-owner admin privileges. 
   2. Then, create a role for the bot (or a generic bot role) and give it the necessary operational permissions (which I will detail later).
   3. Finally, through the server settings, navigate to Integrations and specify the channels where the bot is allowed 

## Local Run
1.  Ensure you have a .env file in the compend directory that matches env.template with values filled in based on your setup
    1. REDIS_PASSPHRASE is up to you
2. Install the library by navigating to `this-advantage/compend` and running `poetry install`
3. Spin up necessary services with `docker compose up`
4. Run the bot with `poetry run python bot.py`


## Local Debug
You should be okay with targeting the bot file and including the local .env, e.g. in VsCode:
```json
    {
        "name": "Python: Inspect Compend Bot",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/compend/bot.py",
        "console": "integratedTerminal",
        "envFile": "${workspaceFolder}/compend/.env",
        "justMyCode": true
    }
```

## Commands