import discord
from discord.ext import commands
from discord.app import option
from engine import Game

from utils.botbase import HungerGamesBot
from utils.errors import *
from utils.checks import *

from config import Config

bot = HungerGamesBot(Config())

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.ApplicationCommandInvokeError):
        error = error.original
    if isinstance(error, HungerGamesError):
        return await ctx.respond(error, ephemeral=True)
    elif isinstance(error, (commands.CheckFailure, discord.app.errors.CheckFailure)):
        pass
    else:
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
@game_exists()
async def register(ctx):
    """
    Register as a tribute for the Hunger Games.
    """

    game = bot.hunger_games[ctx.guild.id]
    result = await game.add_contestant(ctx.author)
    if result:
        await ctx.respond("You have registered as tribute. May the odds be ever in your favour.")
    else:
        await ctx.respond("You are already registered as a tribute.", ephemeral=True)

@bot.slash_command()
@is_registered()
async def inventory(ctx):
    await ctx.respond('Your inventory is empty', ephemeral=True)