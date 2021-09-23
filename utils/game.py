import asyncio
import discord

from engine import GameEngine, Prompt

class Game:
    """The Class that manages interactions with the Bot"""

    def __init__(self, bot, contestant_role):
        self.bot = bot
        self.guild = contestant_role.guild
        self.contestant_role = contestant_role


        self.engine = GameEngine()
        self.players = []
        self.running = False
    
    async def add_contestant(self, member):
        if member in self.players:
            return False
        self.engine.add_player(member)
        self.players.append(member)
        await member.add_roles(self.contestant_role)
        return True

    def create_stats_embed(self, member):
        embed = discord.Embed(title=f"{member.name}'s stats", color=discord.Color.yellow())
        player = self.engine.players[member.id]
        
        embed.description = '\n'.join([
            f'💪 Strength: {player.strength}',
            f'🍖 Hunger: {player.hunger}',
            f'💧 Thirst: {player.thirst}',
        ])
        embed.set_footer(text="Tip: If your hunger or thirst goes over 100, you'll die!")
        return embed

    def create_tributes_embed(self):
        embed = discord.Embed(title=f"Tributes List", color=discord.Color.yellow())
        embed.description = ""
        for p in self.engine.players.values():
            text = f'<@{p.id}>'
            if p.dead:
                text = f"~~{text}~~"
            
            embed.description += text + '\n'
        return embed


    async def run(self, ctx):
        self.running = True
        self.ctx = ctx
        self.engine.setup()
        embed = discord.Embed(
            description='The Hunger Games will begin in 30 seconds!\n\nMeanwhile you can view your base stats with `/stats` or view the map with `/map`.',
            color=discord.Color.yellow()
        )
        embed.set_image(url='https://c.tenor.com/CmDEZGSdu4UAAAAC/jennifer-lawrence-the-mocking-jay.gif')
        await ctx.respond(
            self.contestant_role.mention, 
            embed=embed, 
            allowed_mentions=discord.AllowedMentions(roles=True)
        )
        #await asyncio.sleep(30)
        
        for day in range(2):
            await self.start_day(day)
        self.running = False

    async def start_day(self, day):
        self.engine.start_day(day)
        
        view = StartButton(self)
        await self.ctx.send(f'Day {day} begins. Press the red button to begin.', view=view)
        await self.progress_day()

    async def end_day(self):
        # Winner needs to be checked here 
        
        await self.ctx.send(f'Day {self.engine.current_day.date} ends. These people died today. The next day will begin soon!', embed=self.create_tributes_embed())
        self.engine.end_day()

    async def progress_day(self):
        for _ in range(20):
            self.engine.progress_day(5)
            await asyncio.sleep(10)

        await self.end_day()

    def prompt_to_view(self, prompt: Prompt) -> discord.ui.View:
        if prompt.type == 1:
            pass # TODO
        else:
            return SelectOption(self, [str(s) for s in prompt.responses])

    def get_prompt(self, member):
        return self.engine.players[member.id].get_prompt()

    async def handle_response(self, interaction, response):
        self.engine.players[interaction.user.id].add_response(response)
        await interaction.response.edit_message(content='yeah boi')
        # TODO

class StartButton(discord.ui.View):
    def __init__(self, game):
        super().__init__()
        self.game = game

    @discord.ui.button(emoji='<:hunger_games_salute:890277338263224340>', style=discord.ButtonStyle.red)
    async def button_callback(self, button, interaction):
        e = self.game.engine.current_day
        r = self.game.get_prompt(interaction.user)
        await interaction.response.send_message(
            f"{r}. Current Time: {e} {e.time}",
            view=self.game.prompt_to_view(r),
            ephemeral=True
        )

    async def interaction_check(self, interaction):
        if not interaction.user in self.game.players:
            await interaction.response.send_message("You are not a tribute and cannot participate in this hunger games event. Please wait for this to finish.", ephemeral=True)
            return False
        elif self.game.engine.players[interaction.user.id].dead:
            await interaction.response.send_message("You are dead. You'll have to wait for this game to end before registering again.", ephemeral=True)
            return False
        return True

class SelectOption(discord.ui.View):
    def __init__(self, game, options):
        super().__init__()
        final_options = []
        for option in options:
            if isinstance(option, str):
                final_options.append(discord.SelectOption(label=option))
            else:
                final_options.append(discord.SelectOption(label=option[0], emoji=option[1]))

        self.select = discord.ui.Select(placeholder='What will you do?', options=final_options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        self.game = game

    async def select_callback(self, interaction):
        await self.game.handle_response(interaction, self.select.values[0])




    