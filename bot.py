import discord
from discord.ext import commands

from config import Config


class HungerGamesBot(commands.Bot):
    def __init__(self):
        self.config = Config()
        super().__init__(
            command_prefix=self.config.default_prefix,
            case_insensitive=True,
            description="The Hunger Games bot",
            allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False),
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="people kill each other"
            ),
        )

        self.load_extension('jishaku')

    def run(self):
        super().run(self.config.bot_token)

bot = HungerGamesBot()

@bot.event
async def on_ready():
    print(f'Hunger Games Bot v{bot.config.version} is ready')
    print(f'Logged in as {bot.user}')

@bot.slash_command()
async def info(ctx):
    await ctx.respond('Hello')