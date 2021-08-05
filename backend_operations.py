import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from dotenv import load_dotenv
import json as js

global data

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=["$"])


def load_data_file():
    with open("data.json") as data_file:
        return json.loads(data_file.read())


def dump_data():
    with open("data.json") as file:
        json.dump(data, file)



"""@bot.command(name="shell-run")
async def shell(ctx, cmd_var: str):
    out = os.popen(cmd_var)
    await ctx.channel.send(f"The output is: {out.read()}")"""

bot.run(TOKEN)
