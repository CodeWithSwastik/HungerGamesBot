import discord
from discord.ext import commands
from discord.app import option
from engine import Game

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
@option('role', description="The Contestant Role", required=False)
@commands.has_permissions(administrator=True)
async def setup(ctx, role: discord.Role):
    """
    Setup a new instance of the Hunger Games.
    """
    role = role or discord.utils.get(ctx.guild.roles, name='Contestant')
    await bot.create_game(role)
    await ctx.respond("Hello admin, I have created an instance of the Hunger games for your server.")

@bot.slash_command()
async def register(ctx):
    """
    Register as a tribute for the Hunger Games.
    """
    if ctx.guild.id not in bot.hunger_games:
        return await ctx.respond("There is no active hunger games on going at the moment in this server. Please ask an administrator to setup a game.", ephemeral=True)
    game = bot.hunger_games[ctx.guild.id]
    result = await game.add_contestant(ctx.author)
    if result:
        await ctx.respond("You have registered as tribute. May the odds be with you.")
    else:
        await ctx.respond("You are already registered as a tribute.", ephemeral=True)