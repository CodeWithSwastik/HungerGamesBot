import discord
from discord.ext import commands

from utils.botbase import HungerGamesBot
from utils.errors import *

from config import Config

bot = HungerGamesBot(Config())

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.ApplicationCommandInvokeError):
        error = error.original
    if isinstance(error, HungerGamesError):
        pass
    
    await ctx.respond(f'An unknown error occurred: {error}', ephemeral=True)
    raise error

@bot.slash_command()
@commands.has_role('Admin')
async def info(ctx):
    await ctx.respond("Hello admin")