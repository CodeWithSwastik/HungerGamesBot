import discord
from engine import GameEngine

class Game:
    """The Class that manages interactions with the Bot"""

    def __init__(self, bot, contestant_role):
        self.bot = bot
        self.guild = contestant_role.guild
        self.contestant_role = contestant_role


        self.engine = GameEngine()
        self.players = []
    
    async def add_contestant(self, member):
        if member in self.players:
            return False
        self.engine.add_player(member)
        self.players.append(member)
        await member.add_roles(self.contestant_role)
        return True

    def create_stats_embed(self, member):
        embed = discord.Embed(title=f"{member.name}'s stats", color=discord.Color.yellow())
        return embed

    async def run(self, ctx):
        self.ctx = ctx
        return True