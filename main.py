"""
This is a Discord Bot created by Joshua Estes and Logan Gordy.
Use of this bot must comply with Discord ToS and other government regulations.
Release Date: October 27, 2020

Disclaimer:
Me or my fellow associates are not liable for any mishandling of the
bot by any other foreign entities, sole responsibility will be on the user of said
program.
"""

import backend_operations
import datetime
import os
import random as r
from datetime import date
import discord
import googletrans
import robin_stocks as robin
import pyotp
from discord_slash import SlashCommand
from discord.ext import commands
from dotenv import load_dotenv
from googlesearch import search
from googletrans import Translator
from GoogleBot_PyFiles import encryption_cmd as cmd, googletranslang, stocks
from GoogleBot_PyFiles import color

from time import sleep
from discord import FFmpegPCMAudio
from discord.utils import get
from pretty_help import PrettyHelp
from BiblePackage import BibleGet
import asyncio
from discord_slash.utils.manage_commands import create_option

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')

guild_ids = [755434504457420862, 842460244797030471, 799054655648169994, 798985250595405884, 745665032573943889,
             765806061339803679, 750163999638945872]

bot = commands.Bot(command_prefix=["Hey Google, ", "$ ", "<> "], help_command=PrettyHelp())
slash = SlashCommand(bot, sync_commands=True)
today = date.today()
Discord_ID = '<@!610469915442282526> or DarthBane#8863'
version_num = '2.7.3'


@bot.event
async def on_ready():
    channel = bot.get_channel(756568695320608910)  # Gets the channel with this channel id
    print(f'{bot.user.name} has connected to Discord')  # Sends an online message to the command line
    await bot.change_presence(activity=discord.Game(name="search and record"))
    # Sends an online message to the aforementioned channel
    message = await channel.send(f'{bot.user.name} has connected to discord')
    msg = 'WolframLanguageSession Initialized'
    await message.edit(content=f"{bot.user.name} has connected to discord\n{msg}")
    embed_var = discord.Embed(title='Thank you for using me!', description="Powered by:", color=0xff000b)
    embed_var.set_thumbnail(url='https://www.python.org/static/community_logos/python-logo-master-v3-TM.png')
    await message.edit(embed=embed_var)  # Send a thank you message with a powered by Python message

    backend_operations.load_data_file()
    backend_operations.data["running"] = True
    backend_operations.dump_data()

    @slash.slash(name="describe", guild_ids=guild_ids, options=[
        create_option(name="arg", description="Non-req argument", option_type=3, required=False)
    ])
    async def _describe(ctx, arg):
        description_msg = f'I am a Discord bot created by Joshua Estes and Logan Gordy in an ' \
                          f'effort to make a bot that can do an assortment of different task determine ' \
                          f'by the users. I am currently on version {version_num}. Try "Hey Google, help" to ' \
                          f'get started.'
        embed_var = discord.Embed(title='Who am I?', description=description_msg, color=0x00ff00)
        embed_var.set_thumbnail(url='https://th.bing.com/th/id/OIP.7ZvVP00p4WDHmErvpPw88gHaHa?pid=Api&rs=1')
        await ctx.channel.send(embed=embed_var)


@bot.command(name='get', aliases=['robin'], help='Takes stock symbol, returns price\n[Hey Google | "$ " | "<> "] [get |'
                                                 ' robin] [common | crypto | pharma | <stock name>] '
                                                 'if crypto[-f | -s <crypto name>] [description]')
async def load_stock(ctx, *, arg=None):
    totp = pyotp.TOTP("ODWNVJJZLZIOJB6F").now()
    robin.robinhood.login(username, password, mfa_code=totp)
    stocks_n = None
    everything = None
    crypto_modifier = None
    embed_var = None
    if arg is None:
        msg = "Im sorry, but I need the symbol for the stock you are looking for, please try again. " \
              "If you think I made a mistake, please contact <@!610469915442282526>  to resolve this issue"
        await ctx.channel.send(f'{msg}')
    else:
        option_str = arg.split()
        if len(option_str) == 1:
            option = option_str[0]

        elif len(option_str) == 2:
            option = option_str[0]
            stocks_n = option_str[1]

        elif len(option_str) == 3:
            option = option_str[0]
            stocks_n = option_str[1]
            crypto_modifier = option_str[2]

        else:
            option = option_str[0]
            stocks_n = option_str[1]
            everything = option_str[3]

        msg = "Please wait while I compile the information you have requested, approximately 2 to 3 seconds"
        message = await ctx.channel.send(f'{msg}')
        # await discord.channel.TextChannel.trigger_typing(self=ctx)

        if option == 'common':
            if everything == 'everything':
                final_msg = stocks.LoadStock().common_everything()
                embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
            else:
                final_msg = stocks.LoadStock().common()
                embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])

        elif option == 'crypto':
            if crypto_modifier is None:

                if stocks_n == '-f':
                    final_msg = stocks.LoadStock.crypto_stock()
                    embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
                    embed_var.set_thumbnail(url=final_msg[3])

            else:
                if stocks_n == '-s':
                    final_msg = stocks.LoadStock(stocks=crypto_modifier).crypto()
                    if len(final_msg) == 4:
                        embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
                        embed_var.set_thumbnail(url=final_msg[3])
                    else:
                        embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])

                else:
                    final_msg = stocks.LoadStock(stocks=stocks_n, crypto_modifier=crypto_modifier).crypto()
                    if len(final_msg) == 4:
                        embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
                        embed_var.set_thumbnail(url=final_msg[3])
                    else:
                        embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])

        elif option == 'pharma':
            final_msg = stocks.LoadStock.pharma_stock()
            embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
            embed_var.set_thumbnail(url=final_msg[3])

        else:
            if stocks_n == 'description':
                final_msg = stocks.LoadStock(option=option).stock_description()
                if len(final_msg) == 4:
                    embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
                    embed_var.set_thumbnail(url=final_msg[3])
                else:
                    embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])

            else:
                final_msg = stocks.LoadStock(option=option).stock()
                if len(final_msg) == 4:
                    embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
                    embed_var.set_thumbnail(url=final_msg[3])
                else:
                    embed_var = discord.Embed(title=final_msg[0], description=final_msg[1], color=final_msg[2])
        await asyncio.sleep(2)
        await message.edit(embed=embed_var, content="")


@bot.command(name='add', help='Adds a symbol to the common stock list')
async def mutation(ctx, *, arg):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    stocks_n = arg.split()
    for words in stocks_n:
        with open("../GoogleBot-Cogs/common-stock-list.txt", 'a') as f:
            f.write(f'{words}\n')
            f.close()
    await ctx.channel.send("Success")


@bot.command(name='hello', aliases=['hi', 'hola', 'sup'], help='Says hello back')
async def on_message(message):
    await discord.channel.TextChannel.trigger_typing(self=message)
    hello_dictionary = {
        1: 'Hello Mad Lad',
        2: 'Howdy Partner',
        3: "Ello gov'na",
        4: "Sup Bruh",
        5: "こんにちは",
        6: "Go away",
        7: "ねじオフ"
    }
    x = hello_dictionary[r.randint(1, 7)]
    await message.channel.send(f'{x}')
    # Sends Hello mad lad after the user prompts it in discord


@bot.command(name='list', help='"encryption options"')
async def show(ctx, *, arg):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    choices = 'base84\n' \
              'base64\n' \
              'base32\n' \
              'base16\n' \
              'SHA256\n' \
              'SHA384\n' \
              'SHA512\n' \
              'blake2b\n' \
              'md5'
    await ctx.channel.send(f'When using the encode command, choices are case sensitive.\n {choices}')


@bot.command(name='encode', help='syntax: encode <String> using <choice of encryption>')
async def encode(ctx, *, arg):
    string_list = arg.split()
    encode_string = ''
    for word in string_list:
        if word.lower() != 'using':
            encode_string += word
        if word.lower() == 'using':
            break
    num = len(string_list) - 1
    method = string_list[num]
    encode_s = cmd.EncodeString
    encrypted_string = encode_s.switch(cmd.EncodeString(encode_string), method).string
    await ctx.channel.send(f'{encrypted_string}')


@bot.command(name='echo', help='Echos back user input')
async def echo(ctx, *, arg):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    await ctx.channel.send(f'{arg}')


@bot.command(name='AddSaying')
async def add_saying(ctx, *, arg):
    with open('Banned_sayings.txt', 'a') as BFile:
        BFile.write(arg)
        msg = 'The operation was completed successfully'
        await ctx.channel.send(f'{msg}\n')


@bot.command(name='announce', help='Allows announcement to be used')
async def ann(ctx, user_input: str, channel_id: int, delete=False):
    await ctx.channel.send("Request received: executing now")
    channel = bot.get_channel(channel_id)
    if delete is True:
        await channel.send(f'{user_input} {str(delete)}')
    else:
        await channel.send(f'{user_input}')
    # Echos user input


audio_dict = {
    1: 'playme.mp3',
    2: 'PlayMe2.mp3'
}
meme_dictionary = {
    1: 'Hello There',
    2: '*Nani*',
    3: 'Boi if you don\'t get that out of here',
    4: '*China*'
}


@bot.command(name='send', help='syntax: send me memes. Shows an image')
async def image(ctx, *, arg):
    command = arg.split()
    type_f = None
    choice = None
    print(command)
    if len(command) == 3:
        type_f = command[2]
    if len(command) == 4:
        type_f = command[2]
        choice = command[3]
    print(type_f)
    d1 = today.strftime("%m/%d/%Y")  # Gets current date
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    if d1 == "09/11/2001":
        await ctx.channel.send(file=discord.File('Images/image4.jpg'))
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(file=discord.File('Images/image2.jpg'))
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(file=discord.File('Images/image3.jpg'))
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(file=discord.File('Images/image1.jpg'))
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(file=discord.File('Images/image.jpg'))
    elif type_f is not None:
        if type_f == 'mp3':
            try:
                file = audio_dict[int(choice)]
            except TypeError as e:
                rand_int = r.randint(1, 2)
                file = audio_dict[rand_int]
            await ctx.channel.send(file=discord.File(f'Audio/{file}'))
        if type_f == 'gif':
            await ctx.channel.send(file=discord.File('GIF/258c8822b6a11bdc8d0060bd9bb47df3.gif'))
    else:
        x1 = str(r.randint(6, 16))
        await ctx.channel.send(file=discord.File(f'Images/image{x1}.jpg'))


@bot.command(name='bible', help='syntax=<book><chapter><start-verse><optional: end-verse>')
async def GetBibleVerse(ctx, book_name: str, chapter: int, verse: int, last_verse=0):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    var = BibleGet.bibleVerse(book_name, chapter, verse, last_verse)

    embed_var = discord.Embed(title=var[0], description=var[1], color=var[2])
    await ctx.channel.send(embed=embed_var)


@bot.command(name='date', help='Returns the current date')
async def date(ctx, object2: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    if object2 == '-d':
        d1 = today.strftime("%m/%d/%Y")
        await ctx.channel.send(d1)
    elif object2 == "-t":
        current = datetime.datetime.now()
        d2 = current.strftime("%I:%M:%S %p")
        await ctx.channel.send(d2)
    else:
        d1 = today.strftime("%m/%d/%Y")
        current = datetime.datetime.now().strftime("%I:%M:%S %p")
        await ctx.channel.send(f"The current date and time is: {d1} {current}")


@bot.command(name='google', help='Googles the term specified (place in quotes)')
async def google(ctx, *, query: str):
    wait_message = "Please wait while I gather the top ten search results."
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    message = await ctx.channel.send(wait_message)
    results = ''
    for j in search(query, tld="co.in", stop=10, pause=2):
        results += "<" + j + ">\n"

    await message.edit(content=f"{results}")


@bot.command(name='evaluate', help='evaluates line of code given')
async def evaluate(ctx, code: str):
    if code == "help" or code == "help()":
        await ctx.channel.send(f"I'm sorry, but {code} is not a valid argument for this function")
    g3 = eval(code)
    await ctx.channel.send(f'{g3}')


@bot.command(name='translate', help='Translates a string to another language')
async def translate(ctx, user_input: str, trans_lang=None):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    if user_input == 'list':
        msg = googletranslang.discord_msg()
        embed = discord.Embed(title='List of all languages', description=msg, color=0xff0000)
        await ctx.channel.send(embed=embed)
    else:
        translator = Translator()
        list_lang = googletrans.LANGCODES
        translations = translator.translate([user_input], dest=list_lang[trans_lang])
        for translation in translations:
            msg = translation.origin + ' ----> ' + translation.text
            error_msg = 'The section of text you want to translate makes the message over 2000 characters, ' \
                        'please shorten it'
            if len(msg) > 2000:
                await ctx.channel.send(f'{error_msg}')
            else:
                embed_var = discord.Embed(title=f'Translation to {trans_lang}', description=msg, color=0x00ff00)
                await ctx.channel.send(embed=embed_var)


@bot.command(name='roll', help='Rolls a dice')
async def roll(ctx, dice_type: str):
    dice_type1 = dice_type.lower()
    num = int(dice_type1.replace("d", ""))
    result = r.randint(1, num)
    await ctx.channel.send(f'{result}')


@bot.command(name='join', help='join a voice channel and plays a sound')
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError as e:
        error_msg = 'You are not currently in a channel, therefore I can not join you.' \
                    'Please join a channel then try again.'
        await ctx.channel.send(f'{error_msg}\nError code: {e}')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    audio_dir = 'Audio/playme.mp3'
    source = FFmpegPCMAudio(audio_dir)
    voice.play(source)
    sleep(27)
    await ctx.voice_client.disconnect()


@bot.command(name='leave')
async def leave_guild(ctx):
    if ctx.author.id == 610469915442282526:
        await discord.guild.Guild.leave(ctx.guild)
    else:
        msg = "You are not allowed to use this function"
        await ctx.channel.send(msg)


@bot.command(name='compile')
async def resources(ctx, title, links):
    embed_var = discord.Embed(title=title, description=links, color=0xff0000)
    embed_var.set_thumbnail(url='https://london.ac.uk/sites/default/files/styles/max_1300x1300/public/2018-03/da'
                                'ta-science.jpg?itok=bTPDs5nf')
    await ctx.channel.send(embed=embed_var)


@bot.command(name='kys')
async def kys(ctx):
    await ctx.channel.send('lol')


@bot.command(name='kek', aliases=['kms', 'bs'])
async def derp(ctx, *, arg):
    punctuation = [',', '.', '`', '!', '@', '#', '$', '%', '^', '&', '*', '()', '_', '+', '{', '}', '|', ':', '"', '<',
                   '>', '?', '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', ';']
    ret = []
    lower = False
    upper = True
    for letter in arg:
        if letter == " ":
            ret.append(letter)
        elif letter in punctuation:
            ret.append(letter)
        elif lower:
            lower = False
            upper = True
            ret.append(letter.lower())
        elif upper:
            upper = False
            lower = True
            ret.append(letter.upper())

    await ctx.channel.send("".join(ret))


perms_error = "I am sorry, but I do not have the permissions to proceed with this command. " \
              "If you believe that there is a mistake, contact the admins or <@!610469915442282526>. " \
              "Thank you"


@bot.command(name="add_color")
async def add_role(ctx, hex_color):
    for role in ctx.author.roles:
        if role.name[0] == "#" and color.is_valid_hex(role.name[1:]):
            await ctx.channel.send("You already have a color!")
            return
    if not color.is_valid_hex(hex_color):
        if hex_color.startswith("#"):
            await ctx.channel.send("You didn't supply a valid number")
        else:
            await ctx.channel.send("Didn't start with a #")
        return
    color_code = int(hex_color[1:].upper(), 16)
    try:
        role = await ctx.guild.create_role(name=hex_color, color=discord.Color(color_code))
        await ctx.message.author.add_roles(role)
        await ctx.channel.send(f"Added {hex_color} to <@!{ctx.author.id}>")
    except discord.errors.Forbidden:
        await ctx.channel.send(perms_error)


@bot.command(name="remove_color")
async def remove_role(ctx):
    roles = ctx.message.author.roles
    for role in roles:
        if color.is_valid_hex(role.name):
            try:
                await ctx.author.remove_roles(role)
            except discord.errors.Forbidden:
                await ctx.channel.send(perms_error)
            await ctx.channel.send(f"removed role {role} from <@!{ctx.author.id}>")


bot.run(TOKEN)

backend_operations.load_data_file()
backend_operations.data["running"] = False
backend_operations.dump_data()
