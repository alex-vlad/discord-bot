import discord
from discord.ext import commands
import random
from discord.utils import get

import datetime as dt
from database import update_bank, get_player, display_shop, add_to_inventory, empty_inventory, display_worry


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_called = None

    @commands.command()
    async def roll(self, ctx):
        """Rolls a random number between 1 and 100"""
        await ctx.send(random.randint(0, 100))

    @commands.command()
    async def worrypm(self, ctx, user: discord.User):
        """PM someone a nice worry."""
        emoji = get(ctx.message.guild.emojis, name='worry')
        await user.send(emoji)

    @commands.command()
    async def worry(self, ctx):
        """Just worry."""
        emoji = get(ctx.message.guild.emojis, name='worry')
        await ctx.send(emoji)
        update_bank(ctx.message.author, 1)

    @commands.command(name='stats')
    async def stats(self, ctx):
        """Check your inventory."""
        player = get_player(ctx.message.author.id)
        await ctx.send("Joined server: %s\nBank Account: %s coins\nInventory: 1.%s\n2.%s\n3.%s\n4.%s"
                       % (player['join_server_date'], player['bank'], player['inventory_slot_one'],
                          player['inventory_slot_two'], player['inventory_slot_three'], player['inventory_slot_four']))

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.last_called and dt.datetime.now() < self.last_called + dt.timedelta(seconds=1000):
            return
        else:
            self.last_called = dt.datetime.now()
            update_bank(message.author, 50)
            await message.channel.send(message.author.mention + " You won 50 coins.")

    @commands.command(name='shop')
    async def shop(self, ctx):
        """Items shop"""
        item = display_shop()
        await ctx.send("Shop:")
        for element in item:
            await ctx.send(element)

    @commands.command(name='buy')
    async def buy(self, ctx, item_id):
        """Buy an item from the shop using the ID"""
        player = get_player(ctx.message.author.id)
        item = display_shop()
        if player['inventory_slot_one'] is None or player['inventory_slot_two'] is None \
                or player['inventory_slot_three'] is None or player['inventory_slot_four'] is None:
            for element in item:
                if element['ID'] == int(item_id):
                    item = element['Item']
                    member = ctx.message.author
                    add_to_inventory(member, item)
                    price = element['Price']
                    update_bank(member, -int(price))
                    await ctx.send("You bought %s" % (element['Item']))
        else:
            await ctx.send("Your inventory is full")

    @commands.command()
    async def remove(self, ctx, slot):
        """Remove one item from inventory."""
        member = ctx.message.author
        empty_inventory(member, int(slot))
        await ctx.send("Item removed")

    @commands.command()
    async def craft_table(self, ctx):
        """Available crafts and requirements."""
        emoji = get(ctx.message.guild.emojis, name='worry')
        emoji3 = get(ctx.message.guild.emojis, name='worrythanos')
        emoji2 = get(ctx.message.guild.emojis, name='worrycool')
        emoji4 = get(ctx.message.guild.emojis, name='waifuworry')
        emoji5 = get(ctx.message.guild.emojis, name='worrywe')
        emoji6 = get(ctx.message.guild.emojis, name='worrythink')
        await ctx.send("1.{} = :eyeglasses: + {}\n"
                       "2.{} = :gloves: + {}\n"
                       "3.{} = :female_sign: + {}\n"
                       "4.{} = :snowflake: + {}\n"
                       "5.{} = :books: + {}".format(emoji2, emoji, emoji3, emoji, emoji4, emoji, emoji5, emoji,
                                                    emoji6, emoji))

    @commands.command()
    async def craft(self, ctx, hero_id):
        """Craft your favorite hero"""
        player = get_player(ctx.message.author.id)
        hero = display_worry()
        if player['inventory_slot_one'] is None or player['inventory_slot_two'] is None \
                or player['inventory_slot_three'] is None or player['inventory_slot_four'] is None:
            for element in hero:
                if element['ID'] == int(hero_id):
                    item1 = element['Item1']
                    item2 = element['Item2']
                    worry = element['Worry']
                    member = ctx.message.author
                    if (player['inventory_slot_one'] == item1 or player['inventory_slot_two'] == item1 or
                        player['inventory_slot_three'] == item1 or player['inventory_slot_four'] == item1) and (
                            player['inventory_slot_one'] == item2 or player['inventory_slot_two'] == item2 or
                            player['inventory_slot_three'] == item2 or player['inventory_slot_four'] == item2):
                        add_to_inventory(member, worry)
                        await ctx.send('Craft successful')
                    else:
                        await ctx.send("You don't have the necessary items. Check craft table for more info.")
        else:
            await ctx.send("Your inventory is full")

    @commands.command(name='gc')
    async def give_coins(self, ctx, user: discord.User, amount):
        """Transfer coins to another member"""
        member = ctx.message.author
        update_bank(member, -int(amount))
        update_bank(user, int(amount))
        await ctx.send("Transferred {} coins to {}".format(amount, user.mention))


def setup(bot):
    bot.add_cog(Fun(bot))
