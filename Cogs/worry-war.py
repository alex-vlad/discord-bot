import random
import time
import discord
from discord.ext import commands
from discord.utils import get

from database import get_player


class Player:

    def __init__(self, name):
        self.health = 1000000
        self.name = name
        self.intensifier = 35
        self.ultimate = 'Fatal Worry'
        self.ulti_intensifier = 8
        self.heal_intensifier = 10

    async def calculate_damage(self, ctx, damage_amount, attacker, intensifier):
        if damage_amount * intensifier > self.health:
            overkill = abs(self.health - damage_amount * intensifier)
            self.health = 0

            if overkill > 0:
                await ctx.send("{0} takes fatal damage from {1}, with *{2}* overkill!"
                               .format(self.name, attacker, overkill))
            else:
                await ctx.send("{0} takes fatal damage from {1}!"
                               .format(self.name, attacker))
        else:
            self.health = self.health - (damage_amount * intensifier)
            await ctx.send("{0} takes *{1}* damage from {2}!"
                           .format(self.name, damage_amount * intensifier, attacker))

    async def calculate_heal(self, ctx, heal_amount, heal_intensifier):

        if heal_amount * heal_intensifier + self.health > 1000000:
            self.health = 1000000
            await ctx.send("{0} heals back to full health!".format(self.name))

        else:
            self.health += heal_amount * heal_intensifier
            await ctx.send("{0} heals for {1}!".format(self.name, heal_amount * heal_intensifier))

    async def normal_heal(self, ctx, heal_amount):

        if heal_amount + self.health > 1000000:
            self.health = 1000000
            await ctx.send("{0} heals back to full health!".format(self.name))

        else:
            self.health += heal_amount
            await ctx.send("{0} heals for {1}!".format(self.name, heal_amount))

    async def calculate_ultimate(self, ctx, ulti_dmg, attacker, ulti, ulti_intensifier):
        if ulti_dmg * ulti_intensifier > self.health:
            overkill = abs(self.health - ulti_dmg * ulti_intensifier)
            self.health = 0

            if overkill > 0:
                await ctx.send("{0} takes fatal ultimate {3} damage from {1}, with {2} overkill!"
                               .format(self.name, attacker, overkill, ulti))
            else:
                await ctx.send("{0} takes fatal {2} damage from {1}!"
                               .format(self.name, attacker, ulti))
        else:
            self.health = self.health - ulti_dmg * ulti_intensifier
            await ctx.send("{0} takes {1} damage from {2}!"
                           .format(self.name, ulti_dmg * ulti_intensifier, attacker))


async def get_computer_selection(ctx, health):
    sleep_time = random.randrange(2, 5)
    await ctx.send("*....thinking....*")
    time.sleep(sleep_time)

    if health <= 350000:
        # Have the computer heal ~50% of its turns when <= 350000
        result = random.randint(1, 6)
        if result % 2 == 0:
            return 4
        else:
            return random.randint(1, 3)
    elif health == 1000000:
        return random.randint(1, 3)
    else:
        return random.randint(1, 4)


class WorryWar(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="ww")
    async def worrywar(self, ctx, human1: discord.Member, human2: discord.Member):
        """Two player duel game. Challenge your opponent and engage in a Worry War after selecting your favorite
        worry hero """

        await ctx.send("Welcome to the Worry Wars!")
        emoji = get(ctx.message.guild.emojis, name='worry')
        emoji2 = get(ctx.message.guild.emojis, name='worrythanos')
        emoji3 = get(ctx.message.guild.emojis, name='worrycool')
        emoji4 = get(ctx.message.guild.emojis, name='waifuworry')
        emoji5 = get(ctx.message.guild.emojis, name='worrywe')
        emoji6 = get(ctx.message.guild.emojis, name='worrythink')

        await ctx.send("%s Select your hero:" % human1.mention)
        await ctx.send("For {} press 1.\n"
                       "For {} press 2.\n"
                       "For {} press 3.\n"
                       "For {} press 4.\n"
                       "For {} press 5.\n"
                       "For {} press 6.\n".format(emoji, emoji2, emoji3, emoji4, emoji5, emoji6))
        await ctx.send("Please enter your choice: ")

        def check(m):
            return (m.content == '1' or m.content == '2' or m.content == '3' or
                    m.content == '4' or m.content == '5' or m.content == '6') and \
                   m.channel == ctx.channel and m.author == human1

        async def get_input_of_type():
            while True:
                try:
                    msg = await self.bot.wait_for('message', check=check)
                    return int(msg.content)
                except ValueError:
                    continue

        player = get_player(human1.id)
        hero1 = await get_input_of_type()
        if hero1 == 1:
            if player['inventory_slot_one'] == ':worry:' or player['inventory_slot_two'] == ':worry:' \
                    or player['inventory_slot_three'] == ':worry:' \
                    or player['inventory_slot_four'] == ':worry:':
                ids = human1.id
                human1 = Worry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 2:
            if player['inventory_slot_one'] == ':worrythanos:' or player['inventory_slot_two'] == ':worrythanos:' \
                    or player['inventory_slot_three'] == ':worrythanos:' \
                    or player['inventory_slot_four'] == ':worrythanos:':
                ids = human1.id
                human1 = WorryThanos(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 3:
            if player['inventory_slot_one'] == ':worrycool:' or player['inventory_slot_two'] == ':worrycool:' \
                    or player['inventory_slot_three'] == ':worrycool:' \
                    or player['inventory_slot_four'] == ':worrycool:':
                ids = human1.id
                human1 = WorryCool(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 4:
            if player['inventory_slot_one'] == ':waifuworry:' or player['inventory_slot_two'] == ':waifuworry:' \
                    or player['inventory_slot_three'] == ':waifuworry:' \
                    or player['inventory_slot_four'] == ':waifuworry:':
                ids = human1.id
                human1 = WaifuWorry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 5:
            if player['inventory_slot_one'] == ':worrywe:' or player['inventory_slot_two'] == ':worrywe:' \
                    or player['inventory_slot_three'] == ':worrywe:' \
                    or player['inventory_slot_four'] == ':worrywe:':
                ids = human1.id
                human1 = Worrywe(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 6:
            if player['inventory_slot_one'] == ':worrythink:' or player['inventory_slot_two'] == ':worrythink:' \
                    or player['inventory_slot_three'] == ':worrythink:' \
                    or player['inventory_slot_four'] == ':worrythink:':
                ids = human1.id
                human1 = WorryThink(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return

        await ctx.send("%s Select your hero:" % human2.mention)
        await ctx.send("For {} press 1.\n"
                       "For {} press 2.\n"
                       "For {} press 3.\n"
                       "For {} press 4.\n"
                       "For {} press 5.\n"
                       "For {} press 6.\n".format(emoji, emoji2, emoji3, emoji4, emoji5, emoji6))
        await ctx.send("Please enter your choice: ")

        def check(m):
            return (m.content == '1' or m.content == '2' or m.content == '3' or
                    m.content == '5' or m.content == '5' or m.content == '6') and \
                   m.channel == ctx.channel and m.author == human2

        async def get_input_of_type():
            while True:
                try:
                    msg = await self.bot.wait_for('message', check=check)
                    return int(msg.content)
                except ValueError:
                    continue

        player = get_player(human2.id)
        hero1 = await get_input_of_type()
        if hero1 == 1:
            if player['inventory_slot_one'] == ':worry:' or player['inventory_slot_two'] == ':worry:' \
                    or player['inventory_slot_three'] == ':worry:' \
                    or player['inventory_slot_four'] == ':worry:':
                ids = human2.id
                human2 = Worry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 2:
            if player['inventory_slot_one'] == ':worrythanos:' or player['inventory_slot_two'] == ':worrythanos:' \
                    or player['inventory_slot_three'] == ':worrythanos:' \
                    or player['inventory_slot_four'] == ':worrythanos:':
                ids = human2.id
                human2 = WorryThanos(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 3:
            if player['inventory_slot_one'] == ':worrycool:' or player['inventory_slot_two'] == ':worrycool:' \
                    or player['inventory_slot_three'] == ':worrycool:' \
                    or player['inventory_slot_four'] == ':worrycool:':
                ids = human2.id
                human2 = WorryCool(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 4:
            if player['inventory_slot_one'] == ':waifuworry:' or player['inventory_slot_two'] == ':waifuworry:' \
                    or player['inventory_slot_three'] == ':waifuworry:' \
                    or player['inventory_slot_four'] == ':waifuworry:':
                ids = human2.id
                human2 = WaifuWorry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 5:
            if player['inventory_slot_one'] == ':worrywe:' or player['inventory_slot_two'] == ':worrywe:' \
                    or player['inventory_slot_three'] == ':worrywe:' \
                    or player['inventory_slot_four'] == ':worrywe:':
                ids = human2.id
                human2 = Worrywe(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero1 == 6:
            if player['inventory_slot_one'] == ':worrythink:' or player['inventory_slot_two'] == ':worrythink:' \
                    or player['inventory_slot_three'] == ':worrythink:' \
                    or player['inventory_slot_four'] == ':worrythink:':
                ids = human2.id
                human2 = WorryThink(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return

        game_in_progress = True
        choice = random.randint(0, 1)
        if choice == 1:
            current_player = human1
        else:
            current_player = human2
        while game_in_progress:
            # swap the current player each round
            if current_player == human1:
                current_player = human2
            else:
                current_player = human1
            await ctx.send("%s turn" % current_player.name)
            await ctx.send(
                "{2} has {0} health remaining and "
                "{3} has {1} health remaining.".format(human1.health, human2.health, human1.name, human2.name))
            if current_player == human1:
                await ctx.send("Available attacks: \n"
                               ":one: **Stare** - *Causes moderate damage*\n"
                               ":two: **Lucky Strike** - *high or low damage*\n"
                               ":three: **ULTIMATE**: " + human1.ultimate +
                               "\n:four: **Panacea** - *Restores a moderate amount of health*")
                await ctx.send("Select an attack: ")

                def check(m):
                    return (m.content == '1' or m.content == '2' or m.content == '3' or
                            m.content == '4') and m.channel == ctx.channel and m.author.id == human1.id

                async def get_selection1():
                    while True:
                        try:
                            msg = await self.bot.wait_for('message', check=check)
                            return int(msg.content)
                        except ValueError:
                            continue

                move = await get_selection1()

            else:
                await ctx.send("Available attacks: \n"
                               ":one: **Stare** - *Causes moderate damage*\n"
                               ":two: **Lucky Strike** - *high or low damage*\n"
                               ":three: **ULTIMATE**: " + human2.ultimate +
                               "\n:four: **Panacea** - *Restores a moderate amount of health*")
                await ctx.send("Select an attack: ")

                def check(m):
                    return (m.content == '1' or m.content == '2' or m.content == '3' or
                            m.content == '4') and m.channel == ctx.channel and m.author.id == human2.id

                async def get_selection2():
                    while True:
                        try:
                            msg = await self.bot.wait_for('message', check=check)
                            return int(msg.content)
                        except ValueError:
                            continue

                move = await get_selection2()

            if move == 1:
                damage = random.randrange(1800, 2500)
                if current_player == human1:
                    await human2.calculate_damage(ctx, damage, human1.name, human1.intensifier)
                else:
                    await human1.calculate_damage(ctx, damage, human2.name, human2.intensifier)

            elif move == 2:
                damage = random.randrange(1000, 3500)
                if current_player == human1:
                    await human2.calculate_damage(ctx, damage, human1.name, human1.intensifier)
                else:
                    await human1.calculate_damage(ctx, damage, human2.name, human2.intensifier)

            elif move == 4:
                heal = random.randrange(10000, 15000)
                if current_player == human1 and human1.health < 120000:
                    await human1.calculate_heal(ctx, heal, human1.heal_intensifier)
                elif current_player == human1 and human1.health > 120000:
                    await human1.normal_heal(ctx, heal)
                elif current_player == human2 and human2.health < 120000:
                    await human2.calculate_heal(ctx, heal, human2.heal_intensifier)
                elif current_player == human2 and human2.health > 120000:
                    await human2.normal_heal(ctx, heal)

            elif move == 3:
                if current_player == human1 and human1.health < 150000:
                    damage = random.randrange(10000, 20000)
                    await human2.calculate_ultimate(ctx, damage, human1.name, human1.ultimate, human1.ulti_intensifier)
                elif current_player == human2 and human2.health < 150000:
                    damage = random.randrange(10000, 20000)
                    await human1.calculate_ultimate(ctx, damage, human2.name, human2.ultimate, human2.ulti_intensifier)
                else:
                    await ctx.send("Ultimate is not ready!")
            else:
                await ctx.send("The input was not valid. Please select a choice again.")

            if human1.health == 0 and human2.health > 0:
                await ctx.send("{} you lose".format(human1.name))
                game_in_progress = False
            elif human2.health == 0 and human1.health > 0:
                await ctx.send("{} you lose".format(human2.name))
                game_in_progress = False


class WorryWar2(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="iww")
    async def iworrywar(self, ctx, human: discord.Member):
        """Challenge the Worry AI to a Worry War. Will you be the first to defeat it?"""

        await ctx.send("Welcome to the Worry Wars!")
        computer = Player("**Supreme Worry**")
        emoji = get(ctx.message.guild.emojis, name='worry')
        emoji2 = get(ctx.message.guild.emojis, name='worrythanos')
        emoji3 = get(ctx.message.guild.emojis, name='worrycool')
        emoji4 = get(ctx.message.guild.emojis, name='waifuworry')
        emoji5 = get(ctx.message.guild.emojis, name='worrywe')
        emoji6 = get(ctx.message.guild.emojis, name='worrythink')
        await ctx.send("%s Select your hero:" % human.mention)
        await ctx.send("For {} press 1.\n"
                       "For {} press 2.\n"
                       "For {} press 3.\n"
                       "For {} press 4.\n"
                       "For {} press 5.\n"
                       "For {} press 6.\n".format(emoji, emoji2, emoji3, emoji4, emoji5, emoji6))
        await ctx.send("Please enter your choice: ")

        def check(m):
            return (m.content == '1' or m.content == '2' or m.content == '3' or
                    m.content == '4' or m.content == '5' or m.content == '6') and \
                   m.channel == ctx.channel and m.author == human

        async def get_input_of_type():
            while True:
                try:
                    msg = await self.bot.wait_for('message', check=check)
                    return int(msg.content)
                except ValueError:
                    continue

        player = get_player(human.id)
        hero = await get_input_of_type()
        if hero == 1:
            if player['inventory_slot_one'] == ':worry:' or player['inventory_slot_two'] == ':worry:' \
                    or player['inventory_slot_three'] == ':worry:' \
                    or player['inventory_slot_four'] == ':worry:':
                ids = human.id
                human = Worry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero == 2:
            if player['inventory_slot_one'] == ':worrythanos:' or player['inventory_slot_two'] == ':worrythanos:' \
                    or player['inventory_slot_three'] == ':worrythanos:' \
                    or player['inventory_slot_four'] == ':worrythanos:':
                ids = human.id
                human = WorryThanos(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero == 3:
            if player['inventory_slot_one'] == ':worrycool:' or player['inventory_slot_two'] == ':worrycool:' \
                    or player['inventory_slot_three'] == ':worrycool:' \
                    or player['inventory_slot_four'] == ':worrycool:':
                ids = human.id
                human = WorryCool(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero == 4:
            if player['inventory_slot_one'] == ':waifuworry:' or player['inventory_slot_two'] == ':waifuworry:' \
                    or player['inventory_slot_three'] == ':waifuworry:' \
                    or player['inventory_slot_four'] == ':waifuworry:':
                ids = human.id
                human = WaifuWorry(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero == 5:
            if player['inventory_slot_one'] == ':worrywe:' or player['inventory_slot_two'] == ':worrywe:' \
                    or player['inventory_slot_three'] == ':worrywe:' \
                    or player['inventory_slot_four'] == ':worrywe:':
                ids = human.id
                human = Worrywe(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        elif hero == 6:
            if player['inventory_slot_one'] == ':worrythink:' or player['inventory_slot_two'] == ':worrythink:' \
                    or player['inventory_slot_three'] == ':worrythink:' \
                    or player['inventory_slot_four'] == ':worrythink:':
                ids = human.id
                human = WorryThink(ctx, ids)
            else:
                await ctx.send("You don't own this hero. Please go craft it.")
                return
        game_in_progress = True
        current_player = computer
        while game_in_progress:
            # swap the current player each round
            if current_player == computer:
                current_player = human
            else:
                current_player = computer
            await ctx.send(
                "{2} has *{0}* health remaining and the "
                "**Supreme Worry** has *{1}* health remaining.".format(human.health, computer.health, human.name))
            if current_player == human:
                await ctx.send("Available attacks: \n"
                               ":one: **Stare** - *Causes moderate damage*\n"
                               ":two: **Lucky Strike** - *high or low damage*\n"
                               ":three: **ULTIMATE**: " + human.ultimate +
                               "\n:four: **Panacea** - *Restores a moderate amount of health*")
                await ctx.send("Select an attack: ")

                def check(m):
                    return (m.content == '1' or m.content == '2' or m.content == '3' or
                            m.content == '4') and m.channel == ctx.channel and m.author.id == human.id

                async def get_selection():
                    while True:
                        try:
                            msg = await self.bot.wait_for('message', check=check)
                            return int(msg.content)
                        except ValueError:
                            continue

                move = await get_selection()
            else:
                move = await get_computer_selection(ctx, computer.health)
            if move == 1:
                damage = random.randrange(1800, 2500)
                if current_player == human:
                    await computer.calculate_damage(ctx, damage, human.name, human.intensifier)
                else:
                    await human.calculate_damage(ctx, damage, computer.name, computer.intensifier)
            elif move == 2:
                damage = random.randrange(1000, 3500)
                if current_player == human:
                    await computer.calculate_damage(ctx, damage, human.name, human.intensifier)
                else:
                    await human.calculate_damage(ctx, damage, computer.name, computer.intensifier)
            elif move == 4:
                heal = random.randrange(10000, 15000)
                if current_player == human and human.health < 150000:
                    await human.calculate_heal(ctx, heal, human.heal_intensifier)
                elif current_player == human and human.health > 150000:
                    await human.normal_heal(ctx, heal)
                elif current_player == computer:
                    await computer.calculate_heal(ctx, heal, computer.heal_intensifier)

            elif move == 3:
                if current_player == human and human.health < 150000:
                    damage = random.randrange(10000, 20000)
                    await computer.calculate_ultimate(ctx, damage, human.name, human.ultimate, human.ulti_intensifier)
                elif current_player == computer and computer.health < 150000:
                    damage = random.randrange(10000, 20000)
                    await human.calculate_ultimate(ctx, damage, computer.name, computer.ultimate,
                                                   computer.ulti_intensifier)
                else:
                    await ctx.send("Ultimate not ready!")
            else:
                await ctx.send("The input was not valid. Please select a choice again.")
            if human.health == 0:
                await ctx.send("Sorry, you lose!")
                game_in_progress = False

            if computer.health == 0:
                await ctx.send("Congratulations, you beat the computer!")
                game_in_progress = False


class Worry(Player):

    def __init__(self, ctx, ids):
        self.health = 250000
        emoji = get(ctx.message.guild.emojis, name='worry')
        self.name = emoji
        self.intensifier = 10
        self.ultimate = 'Froggo'
        self.ulti_intensifier = 11.5
        self.id = ids
        self.heal_intensifier = 12


class WorryThanos(Player):

    def __init__(self, ctx, ids):
        self.health = 350000
        emoji = get(ctx.message.guild.emojis, name='worrythanos')
        self.name = emoji
        self.intensifier = 25
        self.ultimate = '*Snap*'
        self.ulti_intensifier = 15
        self.id = ids
        self.heal_intensifier = 5


class WorryCool(Player):

    def __init__(self, ctx, ids):
        self.health = 300000
        emoji = get(ctx.message.guild.emojis, name='worrycool')
        self.name = emoji
        self.intensifier = 20
        self.ultimate = '*Swag*'
        self.ulti_intensifier = 13
        self.id = ids
        self.heal_intensifier = 12.2


class WaifuWorry(Player):

    def __init__(self, ctx, ids):
        self.health = 400000
        emoji = get(ctx.message.guild.emojis, name='waifuworry')
        self.name = emoji
        self.intensifier = 15
        self.ultimate = '*Curative Burst*'
        self.ulti_intensifier = 12.5
        self.id = ids
        self.heal_intensifier = 10


class Worrywe(Player):

    def __init__(self, ctx, ids):
        self.health = 200000
        emoji = get(ctx.message.guild.emojis, name='worrywe')
        self.name = emoji
        self.intensifier = 25.5
        self.ultimate = '*Whatever*'
        self.ulti_intensifier = 12.5
        self.id = ids
        self.heal_intensifier = 1


class WorryThink(Player):

    def __init__(self, ctx, ids):
        self.health = 350000
        emoji = get(ctx.message.guild.emojis, name='worrythink')
        self.name = emoji
        self.intensifier = 26.5
        self.ultimate = '*Outsmarted*'
        self.ulti_intensifier = 14.5
        self.id = ids
        self.heal_intensifier = 7.5


def setup(bot):
    bot.add_cog(WorryWar2(bot))
    bot.add_cog(WorryWar(bot))
