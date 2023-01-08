# bot.py
import os
import sys
import discord
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.INFO)
out_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
out_handler.setFormatter(out_formatter)
logger.addHandler(out_handler)

TOKEN = os.getenv("DISCORD_TOKEN", "")
if not TOKEN:
    logger.error("Missing DISCORD_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")
    

client.run(TOKEN)
