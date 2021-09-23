import discord
from discord.ext import commands
from discord.app import option

from utils import *

from config import Config

bot = HungerGamesBot(Config())

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.ApplicationCommandInvokeError):
        error = error.original
    if isinstance(error, HungerGamesError):
        await ctx.reply(error)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(error)
    elif type(error) in (commands.CheckFailure, discord.app.errors.CheckFailure):
        pass
    else:
        await ctx.reply(f'An unknown error occurred: {error}')
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
    await ctx.respond("I have created an instance of the Hunger games for your server.\nPeople can now `/register` or you can add them using `/add tribute`")

@bot.slash_command()
@game_exists()
async def register(ctx):
    """
    Register as a tribute for the Hunger Games.
    """

    game = bot.get_game(ctx)
    if game.running:
        return await ctx.reply(f"A game is already running in {ctx.channel.mention}, please wait for it to finish before registering.")

    result = await game.add_contestant(ctx.author)
    if result:
        await ctx.respond("You have registered as tribute. May the odds be ever in your favour.")
    else:
        await ctx.reply("You are already registered as a tribute.")

@bot.slash_command()
@option('tribute', description="The member to select as a Tribute")
@game_exists()
@commands.has_permissions(administrator=True)
async def add(ctx, tribute: discord.Member):
    """
    Register as a tribute for the Hunger Games.
    """

    game = bot.get_game(ctx)
    if game.running:
        return await ctx.reply(f"A game is already running in {ctx.channel.mention}, please wait for it to finish before trying to add a tribute.")

    result = await game.add_contestant(tribute)

    if result:
        await ctx.respond(f"{tribute.mention} has been selected as tribute. May the odds be ever in their favour.")
    else:
        await ctx.reply(f"{tribute.mention} is already selected as a tribute.")

@bot.slash_command()
@game_exists()
@commands.has_permissions(administrator=True)
async def start(ctx):
    """Starts the Hunger Games in the channel the command is run."""
    game = bot.get_game(ctx)
    if game.running:
        return await ctx.reply(f"The game is already running in {ctx.channel.mention}, please wait for it to finish before trying to start it.")

    await game.run(ctx)


@bot.slash_command()
@is_registered()
async def inventory(ctx):
    await ctx.reply('Your inventory is empty')

@bot.slash_command()
async def map(ctx):
    """
    Shows the map of the Hunger Games Arena.
    """
    await ctx.respond("Here's the map of the Hunger Games Arena")
    await ctx.send(file=discord.File('map.png'))

@bot.slash_command()
@is_registered()
async def stats(ctx):
    """
    Shows your stats if you are a Tribute.
    """
    embed = bot.get_game(ctx).create_stats_embed(ctx.author)
    await ctx.reply(embed=embed)

@bot.command()
async def source(ctx):
    await ctx.send('https://github.com/CodeWithSwastik/HungerGamesBot')

tribute = bot.command_group('tribute', 'Commands related to Tributes')

@tribute.command(name='list')
@game_exists()
async def list_(ctx):
    """
    Lists all tributes
    """
    embed = bot.get_game(ctx).create_tributes_embed()
    await ctx.reply(embed=embed)


