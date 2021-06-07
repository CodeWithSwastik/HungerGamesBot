import discord
import jishaku
from discord.ext import commands

import os

from config import Config

config = Config()

# Configuring intents
intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(
    command_prefix=config.default_prefix,
    case_insensitive=True,
    description="The Hunger Games bot",
    allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),
    intents=intents
)

# Loading cogs
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.load_extension("jishaku")

if __name__ == "__main__":
    bot.run(config.bot_token)