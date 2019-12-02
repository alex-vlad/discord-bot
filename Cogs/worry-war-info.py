from discord.ext import commands
from discord.utils import get


class WorryWarInfo(commands.Cog):

    @commands.command(name="skills")
    async def skills_info(self, ctx):
        """General information about the Worry War skills"""
        await ctx.send("Available attacks: \n"
                       ":one: **Stare** - *Causes moderate damage*\n"
                       ":two: **Lucky Strike** - *high or low damage*\n"
                       ":three: **ULTIMATE**: "
                       "\n:four: **Panacea** - *Restores a moderate amount of health*")
        await ctx.send("*Stare* base damage: **1800-2500**\n"
                       "*Lucky Strike* base damage: **1000-3500**\n"
                       "*ULTIMATE* base damage: **10000-20000**\n"
                       "*Panacea* base healing: **10000-15000**")


class WorryWarHeroes(commands.Cog):

    @commands.command(name="worrystats")
    async def worry_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='worry')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **10** \n"
                       "*HP*: **250000**\n"
                       "*Ultimate damage intensifier*: **11.5**\n"
                       "*Heal intensifier*: **12**\n"
                       "*Ultimate name*: **Froggo**")

    @commands.command(name="worrythanosstats")
    async def worrythanos_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='worrythanos')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **25** \n"
                       "*HP*: **350000**\n"
                       "*Ultimate damage intensifier*: **15**\n"
                       "*Heal intensifier*: **5**\n"
                       "*Ultimate name*: **Snap**")

    @commands.command(name="worrycoolstats")
    async def worrycool_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='worrycool')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **20** \n"
                       "*HP*: **300000**\n"
                       "*Ultimate damage intensifier*: **13**\n"
                       "*Heal intensifier*: **12.2**\n"
                       "*Ultimate name*: **Swag**")

    @commands.command(name="waifuworrystats")
    async def waifuworry_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='waifuworry')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **15** \n"
                       "*HP*: **400000**\n"
                       "*Ultimate damage intensifier*: **12.5**\n"
                       "*Heal intensifier*: **10**\n"
                       "*Ultimate name*: **Curative Burst**")

    @commands.command(name="worrywestats")
    async def worrywe_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='worrywe')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **25.5** \n"
                       "*HP*: **200000**\n"
                       "*Ultimate damage intensifier*: **12.5**\n"
                       "*Heal intensifier*: **1**\n"
                       "*Ultimate name*: **Whatever**")

    @commands.command(name="worrythinkstats")
    async def worrythink_hero(self, ctx):
        """Summary about the hero's stats"""
        emoji = get(ctx.message.guild.emojis, name='worrythink')
        await ctx.send(emoji)
        await ctx.send("*Damage intensifier*: **26.5** \n"
                       "*HP*: **350000**\n"
                       "*Ultimate damage intensifier*: **14.5**\n"
                       "*Heal intensifier*: **7.5**\n"
                       "*Ultimate name*: **Outsmarted**")


def setup(bot):
    bot.add_cog(WorryWarInfo(bot))
    bot.add_cog(WorryWarHeroes(bot))
