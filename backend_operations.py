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

    @bot.event
    async def on_ready():
        channel = bot.get_channel(756568695320608910)  # Gets the channel with this channel id
        print(f'{bot.user.name} has connected to Discord')  # Sends an online message to the command line
        await bot.change_presence(activity=discord.Game(name="search and record"))
        # Sends an online message to the aforementioned channel
        message = await channel.send(f'{bot.user.name} has connected to discord')
        embed_var = discord.Embed(title='Thank you for using me!', description="Powered by:", color=0xff000b)
        embed_var.set_thumbnail(url='https://www.python.org/static/community_logos/python-logo-master-v3-TM.png')
        await message.edit(embed=embed_var)  # Send a thank you message with a powered by Python message

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
        await ctx.channel.send(var.read())


    @has_permissions(administrator=True)
    @bot.command(name="stop")
    async def stop(ctx):
        dump_data()
        var = os.popen("forever stopall")
        await ctx.channel.send(var.read())


    @has_permissions(administrator=True)
    @bot.command(name="start")
    async def start(ctx):
        dump_data()
        var = os.popen("cd .. && ./start")
        await ctx.channel.send(var.read())

    @has_permissions(administrator=True)
    @bot.command(name="update")
    async def update(ctx):
        dump_data()
        var = os.popen("cd .. && ./update && ./update2")
        await ctx.channel.send(var.read())
    bot.run(TOKEN)