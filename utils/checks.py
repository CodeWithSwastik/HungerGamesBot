from discord.ext import commands
def game_exists():
    async def predicate(ctx):
        if ctx.guild.id not in ctx.bot.hunger_games:
            await ctx.respond("There is no active hunger games on going at the moment in this server. Please ask an administrator to setup a game.", ephemeral=True)
            return False
        return True
    return commands.check(predicate)

def is_registered():
    original = game_exists().predicate
    async def predicate(ctx):
        if not await original(ctx):
            return False
        if ctx.author not in ctx.bot.hunger_games[ctx.guild.id].players:
            await ctx.respond("You can't use this since you haven't registered as a tribute", ephemeral=True)
            return False
        return True
    return commands.check(predicate)
        