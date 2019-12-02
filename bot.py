import os
import logging

from database import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_token = ''

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

items = [{":eyeglasses:": 10000}, {":gloves:": 200000}, {":female_sign:": 50000}, {":snowflake:": 7000}, {":books:": 50000},
         {":worry:": 40000}]

worry = [{":worrycool:": [":worry:", ":eyeglasses:"]}, {":worrythanos:": [":worry:", ":gloves:"]},
         {":waifuworry:": [":worry:", ":female_sign:"]}, {":worrywe:": [":worry:", ":snowflake:"]},
          {":worrythink:": [":worry:", ":books:"]}]


@bot.event
async def on_ready():
    add_all_users_to_db()
    add_all_items_to_shop(items)
    add_all_worry(worry)
    print("[*] Connected to Discord as: " + bot.user.name)


@bot.event
async def on_member_join(member):
    add_user_to_db(member)


bot.run(bot_token)
