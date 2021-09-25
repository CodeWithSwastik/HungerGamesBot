import asyncio
import discord

from engine import GameEngine, Prompt, Battle

class Game:
    """The Class that manages interactions with the Bot"""

    def __init__(self, bot, contestant_role):
        self.bot = bot
        self.guild = contestant_role.guild
        self.contestant_role = contestant_role


        self.engine = GameEngine()
        self.engine.on_player_death = self.on_player_death
        self.players = []
        self.running = False
        self.active_views = []

    async def add_contestant(self, member):
        if member in self.players:
            return False
        self.engine.add_player(member)
        self.players.append(member)
        await member.add_roles(self.contestant_role)
        return True

    def get_member(self, player) -> discord.Member:
        return discord.utils.get(self.players, id=player.id)

    def get_player(self, member):
        return self.engine.players[member.id]


    def create_stats_embed(self, member):
        embed = discord.Embed(title=f"{member.name}'s stats", color=discord.Color.yellow())
        player = self.get_player(member)
        
        embed.description = '\n'.join([
            f'💪 Strength: {player.strength}',
            f'🍖 Hunger: {player.hunger}',
            f'💧 Thirst: {player.thirst}',
            f'❤ Health: {player.health}'
        ])
        if self.running:
            embed.description += '\n'*2
            embed.description += '\n'.join([
                f'🗺 Location: {player.location}',
                f'🏹 Weapons: {player.weapons or None}',
                f'🔪 Killed: {player.killed or None}',
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
        await asyncio.sleep(5)
        
        for day in range(1,10):
            await self.start_day(day)
            if not self.running:
                break
        
        if self.running:
            self.running = False
            self.bot.end_game(self.guild)

    async def start_day(self, day):
        self.interactions = {}
        self.engine.start_day(day)
        
        view = self.create_view(StartButton)
        await self.ctx.send(f'Day {day} begins. Press the red button to begin.', view=view)
        await self.progress_day()

    async def end_day(self):
        embed = discord.Embed(title=f'Day {self.engine.current_day.date} ends', color=discord.Color.red())
        if self.engine.current_day.killed:
            embed.description = "Fallen Tributes:\n"
            embed.description += "\n".join(
                [f"<@{p.id}>" for p in self.engine.current_day.killed]
            )
        else:
            embed.description = "No one died today, but will it be the same tomorrow?"

        self.engine.end_day()
        await self.ctx.send(embed=embed)

        for view in self.active_views:
            if not view.is_finished:
                view.stop()
        
        self.active_views = []

        if self.engine.finished:
            if self.engine.winner is not None:
                winner = self.get_member(self.engine.winner)
                embed = self.get_embed_for(
                    winner,
                    title=f'We have a winner!', 
                    description=f'{winner.mention} has won the Hunger Games!',
                    color=discord.Color.yellow(),
                )
            else:
                embed = discord.Embed(
                    title=f'No one won :(', 
                    color=discord.Color.red()
                )               
            await self.ctx.send(embed=embed)
            await asyncio.sleep(15)
            self.running = False
            self.bot.end_game(self.guild)


    def get_embed_for(self, member, **kwargs):
        embed = discord.Embed(**kwargs)
        embed.set_thumbnail(url=member.display_avatar.url)        
        return embed

    def create_battle_embed(self, player, battle: Battle):
        embed = discord.Embed(color=discord.Color.yellow())
        other = battle.get_other(player)

        e = f'Health: {player.health} ❤ \n'
        e += f'Strength: {player.strength} 💪\n'
        e += f'Weapon: {player.primary_weapon} {player.primary_weapon.emoji}\n'

        embed.add_field(name='Your stats', value=e)

        weapon = other.primary_weapon
    
        e = f'Health: {other.health} ❤ \n'
        e += f'Strength: {other.strength} 💪\n'

        if weapon:
            e += f'Weapon: {weapon} {weapon.emoji}\n'
        else:
            e += f'Weapon: ???\n'
            
        embed.add_field(name=f'{other}\'s stats', value=e)


        return embed

    async def progress_day(self):
        for _ in range(self.engine.current_day.length):
            if not self.engine.progress_day(60): 
                break # day ended early since everyone responded
            await asyncio.sleep(7)

        await self.end_day()

    def prompt_to_view(self, prompt: Prompt) -> discord.ui.View:
        if prompt.type == 1:
            pass # TODO
        else:
            options = [
                str(s)
                if s.emoji is None
                else (str(s), s.emoji)
                for s in prompt.responses
            ]
            return self.create_view(SelectOption, str(prompt), options)

    def get_prompt(self, member):
        return self.get_player(member).get_prompt()

    def on_player_death(self, player, reason):
        member = self.get_member(player)
        async def inner():
            await member.remove_roles(self.contestant_role) 
            embed = self.get_embed_for(member,
                title='A Tribute has fallen', 
                description=f'{player} {reason}', 
                color=discord.Color.red()
            )
            await self.ctx.send(member.mention, embed=embed)
        asyncio.create_task(inner())

    async def handle_response(self, interaction, response):
        self.interactions[interaction.user.id] = interaction
        result = self.engine.add_response(interaction.user.id, response)


        if result.public:
            embed = discord.Embed(
                description=result.public.description, 
                color=result.public.color or discord.Color.random()
            )
            await self.ctx.send(embed=embed)

        if result.battle:
            await self.start_battle(result.battle)
        
        if result.followup:
            # if result.followup.delay:
            #     await asyncio.sleep(result.followup.delay)
            await interaction.response.edit_message(
                content=result.message,
                view = self.prompt_to_view(result.followup)
            )
        else:
            await interaction.response.edit_message(
                content=result.message, view = None
            )
            
        # TODO

    async def start_battle(self, battle: Battle):
        embed = discord.Embed(
            title='Battle ⚔', description=f'{battle.player1} and {battle.player2} get into a fierce battle!'
        )
        embed.set_footer(text='The participants of this battle can press the button to fight')
        await self.ctx.send(
            ' '.join(f'<@{i}>' for i in battle.participants), 
            view=self.create_view(BattleButton, battle)
        )

    async def handle_battle_response(self, interaction, response):
        player = self.get_player(interaction.user)
        battle: Battle = player.battle
        if battle is None:
            return await interaction.response.edit_message(
                content=f'You died.',
                view=None
            )
        other = battle.get_other(player)
        parts = player.body_parts

        if player.primary_weapon is None:
            player.primary_weapon = player.usable_weapons[response]
            await interaction.response.edit_message(
                content=f'You picked your {player.primary_weapon}',
                view=None
            )
            await asyncio.sleep(1)
            
            await interaction.edit_original_message(
                content=f'Where do you attack {other}?',
                view=self.create_view(SelectOption, 'Where do you attack?', parts, battle=True)
            )
        else:
            response = parts[response][0].lower()
            damage_dealt = battle.attack(other, response)
            if other.dead:
                await interaction.response.edit_message(
                    content=f'You killed them! Damage dealt: {damage_dealt}',
                    view=None
                )
            elif damage_dealt is None:
                await interaction.response.edit_message(
                    content=f'You missed the shot!',
                    embed=self.create_battle_embed(player, battle),
                    view=self.create_view(SelectOption, 'Where do you attack next?', parts, battle=True)
                )
            else:
                await interaction.response.edit_message(
                    content=f'Your hit dealt {damage_dealt} damage!',
                    embed=self.create_battle_embed(player, battle),
                    view=self.create_view(SelectOption, 'Where do you attack next?', parts, battle=True)
                )        

    def create_view(self, cls, *args, **kwargs):
        view = cls(self, *args, **kwargs)
        self.active_views.append(view)
        return view          

class StartButton(discord.ui.View):
    # TODO: bug. This button doesn't die when day ends?
    def __init__(self, game):
        super().__init__()
        self.game = game

    @discord.ui.button(emoji='<:hunger_games_salute:890277338263224340>', style=discord.ButtonStyle.red)
    async def button_callback(self, button, interaction):
        e = self.game.engine.current_day
        r = self.game.get_prompt(interaction.user)
        await interaction.response.send_message(
            f"{r}, Current Time: {e}",
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
        elif self.game.engine.players[interaction.user.id].responded:
            await interaction.response.send_message("You have already begun this day.", ephemeral=True)
            return False            
        return True

class SelectOption(discord.ui.View):
    def __init__(self, game, placeholder, options, battle=False):
        super().__init__()
        final_options = []
        for i, option in enumerate(options):
            if isinstance(option, str):
                final_options.append(discord.SelectOption(label=option, value=i))
            else:
                final_options.append(
                    discord.SelectOption(
                        label=option[0], emoji=option[1], value=i
                    ))

        self.select = discord.ui.Select(placeholder=placeholder or 'What will you do?', options=final_options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        self.game = game
        self.battle = battle
    async def select_callback(self, interaction):
        if not self.battle:
            return await self.game.handle_response(interaction, int(self.select.values[0]))
        await self.game.handle_battle_response(interaction, int(self.select.values[0]))

class BattleButton(discord.ui.View):
    def __init__(self, game, battle):
        super().__init__()
        self.game = game
        self.battle = battle
        self.clicked = []
    @discord.ui.button(emoji='⚔', style=discord.ButtonStyle.red)
    async def button_callback(self, button, interaction):
        player = self.game.get_player(interaction.user)

        weapons = [(w.name, w.emoji) for w in player.usable_weapons]

        view = SelectOption(self.game, 'Select a weapon', weapons, battle=True)
        self.game.active_views.append(view)
        await interaction.response.send_message(
            f"Which weapon will you pick to fight in this battle?",
            view=view,
            ephemeral=True
        )

    async def interaction_check(self, interaction):
        if interaction.user.id not in self.battle.participants:
            await interaction.response.send_message("You are not a participant in this battle!", ephemeral=True)
            return False
        if interaction.user in self.clicked:
            await interaction.response.send_message("You already clicked the button!", ephemeral=True)
            return False 
        self.clicked.append(interaction.user)                 
        return True