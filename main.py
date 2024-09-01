import os
import discord

from bot.simple_bot import SimpleBot
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("DISCORD_KEY")
if Token is None:
    print("No key found")
    exit()


intents = discord.Intents().none()
intents.voice_states = True
intents.guilds = True
intents.guild_reactions = True

bot = SimpleBot(intents=intents, command_prefix="/")

bot.run(Token)
