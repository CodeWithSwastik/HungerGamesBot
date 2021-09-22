import discord
from discord.ext import commands

class HungerGamesBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        super().__init__(
            command_prefix=self.config.default_prefix,
            case_insensitive=True,
            description="The Hunger Games bot",
            allowed_mentions=discord.AllowedMentions(
                roles=False, users=True, everyone=False
            ),
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="people kill each other"
            ),
            debug_guild=681882711945641997,
        )

        self.load_extension("jishaku")

    def run(self):
        super().run(self.config.bot_token)

    async def on_ready(self):
        print(f"Hunger Games Bot v{self.config.version} is ready")
        print(f"Logged in as {self.user}")