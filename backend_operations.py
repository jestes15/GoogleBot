import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from dotenv import load_dotenv
import json as js

data = None


def load_data_file():
    global data
    with open("data.json") as data_file:
        data = js.loads(data_file.read())


def dump_data():
    global data
    with open("data.json", "w") as file:
        js.dump(data, file)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix=["$"])


    @has_permissions(administrator=True)
    @bot.command(name="shell-run")
    async def shell(ctx, cmd_var: str):
        out = os.popen(cmd_var)
        await ctx.channel.send(f"The output is: {out.read()}")


    @has_permissions(administrator=True)
    @bot.command(name="restart")
    async def restart(ctx):
        dump_data()
        var = os.popen("cd .. && ./restart")
        await ctx.channel.send(var)


    @has_permissions(administrator=True)
    @bot.command(name="stop")
    async def stop(ctx):
        dump_data()
        var = os.popen("forever stopall")
        await ctx.channel.send(var)


    @has_permissions(administrator=True)
    @bot.command(name="start")
    async def start(ctx):
        dump_data()
        var = os.popen("cd .. && ./start")
        await ctx.channel.send(var)

    @has_permissions(administrator=True)
    @bot.command(name="updatr")
    async def update(ctx):
        dump_data()
        var = os.popen("cd .. && ./update && ./update2")
        await ctx.channel.send(var)
    bot.run(TOKEN)
