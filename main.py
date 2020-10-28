"""
This is a Discord Bot created by Joshua Estes and Logan Gordy.
Use of this bot must comply with Discord ToS and other government regulations.
Release Date: October 27, 2020

Disclaimer:
Me or my fellow associates are not liable for any mishandling of the
bot by any other foreign entities, sole responsibility will be on the user of said
program.
"""


import datetime
import os
import random as r
from datetime import date
import discord
import googletrans
import robin_stocks as robin
from discord.ext import commands
from dotenv import load_dotenv
from googlesearch import search
from googletrans import Translator
from wolframclient.evaluation import WolframLanguageSession
import encryption_cmd as cmd
import stock_images as si

from time import sleep
from discord import FFmpegPCMAudio
from discord.utils import get
from pretty_help import PrettyHelp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')

robin.authentication.login(username, password)

bot = commands.Bot(command_prefix="Hey Google, ", help_command=PrettyHelp())

today = date.today()
session = WolframLanguageSession()

Discord_ID = '<@!610469915442282526> or DarthBane#8863'

version_num = '2.1.0'


@bot.event
async def on_ready():
    channel = bot.get_channel(756568695320608910)  # Gets the channel with this channel id
    print(f'{bot.user.name} has connected to Discord')  # Sends an online message to the command line
    await bot.change_presence(activity=discord.Game(name="search and record"))
    await channel.send(f'{bot.user.name} has connected to discord')
    # Sends an online message to the aforementioned channel
    msg = 'WolframLanguageSession initialized'
    await channel.send(f'{msg}')


@bot.command(name='describe', help='Describes itself or a command.')
async def describe(ctx, *, arg):
    if arg == 'yourself':
        description_msg = f'I am a Discord bot created by Joshua Estes and Logan Gordy in an ' \
                          f'effort to make a bot that can do an assortment of different task determine ' \
                          f'by the users. I am currently on version {version_num}. Try "Hey Google, help" to ' \
                          f'get started.'
        embed_var = discord.Embed(title='Who am I?', description=description_msg, color=0x00ff00)
        embed_var.set_thumbnail(url='https://th.bing.com/th/id/OIP.7ZvVP00p4WDHmErvpPw88gHaHa?pid=Api&rs=1')
        await ctx.channel.send(embed=embed_var)


@bot.command(name='get', help='Takes stock symbol, returns price')
async def load_stock(ctx, *, arg=None):
    stocks = None
    everything = None
    crypto_modifier = None
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
            stocks = option_str[1]

        elif len(option_str) == 3:
            option = option_str[0]
            stocks = option_str[1]
            crypto_modifier = option_str[2]

        else:
            option = option_str[0]
            stocks = option_str[1]
            everything = option_str[3]

        await discord.channel.TextChannel.trigger_typing(self=ctx)

        if option == 'common':
            if everything == 'everything':
                stock_list = {}
                with open('common-stock-list.txt', 'r') as f:
                    array = f.readlines()
                current_date = datetime.datetime.now()
                d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
                stock_list[0] = d2
                msg = "Please wait while I compile the information you have requested, approximately 2 to 3 seconds"
                await ctx.channel.send(f'{msg}')
                await discord.channel.TextChannel.trigger_typing(self=ctx)
                num = 0
                sub = stock_list[0] + '\n'
                while num < (len(array)):
                    string = array[num]
                    stock_price = robin.stocks.get_latest_price(array[num])
                    pb_ratio = robin.stocks.get_fundamentals(array[num], 'pb_ratio')
                    pe_ratio = robin.stocks.get_fundamentals(array[num], 'pe_ratio')
                    dividend_yield = robin.stocks.get_fundamentals(array[num], 'dividend_yield')
                    sub += f'{string[0:-1]}\nPrice = ${stock_price[0]}\nP/B Ratio = {pb_ratio[0]}\nP/E Ratio = {pe_ratio[0]}\nDividend Yield = {dividend_yield[0]}\n\n'
                    num += 1
                embed_var = discord.Embed(title='Common Stocks', description=sub, color=0xff0000)
                await ctx.channel.send(embed=embed_var)
            else:
                stock_list = {}
                with open('common-stock-list.txt', 'r') as f:
                    array = f.readlines()
                current_date = datetime.datetime.now()
                d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
                stock_list[0] = d2
                msg = "Please wait while I compile the information you have requested, approximately 2 to 3 seconds"
                await ctx.channel.send(f'{msg}')
                await discord.channel.TextChannel.trigger_typing(self=ctx)
                num = 0
                sub = stock_list[0] + '\n'
                while num < (len(array)):
                    string = array[num]
                    stock_price = robin.stocks.get_latest_price(array[num])
                    sub += f'{string[0:-1]} = ${str(stock_price[0])}\n'
                    num += 1
                embed_var = discord.Embed(title='Common Stocks', description=sub, color=0xff0000)
                await ctx.channel.send(embed=embed_var)

        elif option == 'crypto':
            if crypto_modifier is None:
                crypto_value = robin.crypto.get_crypto_quote(stocks, 'mark_price')
                if crypto_value is None:
                    error_msg = 'I\'m sorry, but the stock you are looking for is not here, make sure you ' \
                                'are using the correct Id and try again. If you can not figure it out, contact ' \
                                f'the dev of this bot, {Discord_ID}'
                    await ctx.channel.send(error_msg)
                else:
                    current_price = f'The current price of {stocks} is ${crypto_value}'
                    embed_var = discord.Embed(title=f'{"Cryptocurrency"}', description=current_price, color=0x00b300)
                    embed_var.set_thumbnail(url='https://th.bing.com/th/id/OIP.Y25UPylA8mnk-SfKSnEEGQHaFb?pid=Api&rs=1')
                    await ctx.channel.send(embed=embed_var)
            else:
                crypto_value = robin.crypto.get_crypto_quote(stocks, crypto_modifier)
                if crypto_value is None:
                    error_msg = 'I\'m sorry, but the stock you are looking for is not here, make sure you ' \
                                'are using the correct Id and try again. If you can not figure it out, contact ' \
                                f'the dev of this bot, {Discord_ID}'
                    await ctx.channel.send(error_msg)
                else:
                    current_price = f'The {crypto_modifier} of {stocks} is {crypto_value}'
                    embed_var = discord.Embed(title=f'{"Cryptocurrency"}', description=current_price, color=0x00b300)
                    embed_var.set_thumbnail(url='https://th.bing.com/th/id/OIP.Y25UPylA8mnk-SfKSnEEGQHaFb?pid=Api&rs=1')
                    await ctx.channel.send(embed=embed_var)

        else:
            if stocks == 'description':
                description = robin.stocks.get_fundamentals(option, 'description')
                await ctx.channel.send(description[0])
            else:
                stock_info = robin.stocks.get_latest_price(option)
                pb_ratio = robin.stocks.get_fundamentals(option, 'pb_ratio')
                pe_ratio = robin.stocks.get_fundamentals(option, 'pe_ratio')
                dividend_yield = robin.stocks.get_fundamentals(option, 'dividend_yield')
                if stock_info[0] is None:
                    msg = "Im sorry, but the stock you are looking for is not in the archives. " \
                          "If you think I made a mistake, please contact <@!610469915442282526> to resolve this issue"
                    await ctx.channel.send(f'{msg}')
                else:
                    stock_info_number = stock_info[0]
                    msg = f'Price = ${stock_info_number}\nP/B Ratio = {pb_ratio[0]}\nP/E Ratio = {pe_ratio[0]}\n' \
                          f'Dividend Yield = {dividend_yield[0]}'
                    embed_var = discord.Embed(title=f'{option}', description=msg, color=0x00ff00)
                    url = si.load_stock_img(option)
                    embed_var.set_thumbnail(url=url)
                    await ctx.channel.send(embed=embed_var)


@bot.command(name='add', help='Adds a symbol to the common stock list')
async def mutation(ctx, *, arg):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    stocks = arg.split()
    for words in stocks:
        with open("common-stock-list.txt", 'a') as f:
            f.write(f'{words}\n')
            f.close()
    await ctx.channel.send("Success")


@bot.command(name='hello', help='Says hello back')
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
    error_msg = "I'm sorry, that message is not allowed."
    if 'gay' in arg.lower():
        await ctx.channel.send(f'{error_msg}')
    elif 'homo' in arg.lower():
        await ctx.channel.send(f'{error_msg}')
    elif 'fag' in arg.lower():
        await ctx.channel.send(f'{error_msg}')
    elif 'queer' in arg.lower():
        await ctx.channel.send(f'{error_msg}')
    else:
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
            file = audio_dict[int(choice)]
            await ctx.channel.send(file=discord.File(f'Audio/{file}'))
        if type_f == 'gif':
            await ctx.channel.send(file=discord.File('GIF/258c8822b6a11bdc8d0060bd9bb47df3.gif'))
    else:
        x1 = str(r.randint(6, 16))
        await ctx.channel.send(file=discord.File(f'Images/image{x1}.jpg'))


@bot.command(name='search', help='syntax=for <book><chapter><start-verse><optional: end-verse>')
async def GetBibleVerse(ctx, for2: str, book_name: str, chapter: int, verse: int, last_verse=0):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    location = 'Bible/' + book_name + '/' + book_name + '_' + str(chapter) + '.txt'
    with open(location, 'r') as bible:
        bible_read = bible.readlines()

        if last_verse == 0:
            range_verse = f'{book_name} {chapter}:{verse}'
            verse_line = 2 * (verse - 1)
            msg = bible_read[verse_line]
            embed_var = discord.Embed(title=range_verse, description=msg, color=0xffff00)
            await ctx.channel.send(embed=embed_var)

        else:
            i = verse
            i_i = last_verse + 1
            bible_verse = ''
            range_verse = f'{book_name} {chapter}:{verse}-{last_verse}'
            while i < i_i:
                verse_line = 2 * (i - 1)
                bible_verse += bible_read[verse_line] + '\n'
                i += 1
            length = len(bible_verse)
            if length < 2001:
                embed_var = discord.Embed(title=range_verse, description=bible_verse, color=0xffb300)
                await ctx.channel.send(embed=embed_var)
            else:
                msg = "Error: You have requested too many Bible verses " \
                      "and have exceeded the discord limit of 2000 characters " \
                      "please shorten your request and try again."
                await ctx.channel.send(f'{msg}')


@bot.command(name='what', help='Returns the current date')
async def date(ctx, is2: str, the: str, object2: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    if object2 == 'date':
        d1 = today.strftime("%m/%d/%Y")
        await ctx.channel.send(d1)
    else:
        current = datetime.datetime.now()
        d2 = current.strftime("%I:%M:%S %p")
        await ctx.channel.send(d2)


@bot.command(name='google', help='Googles the term specified (place in quotes)')
async def google(ctx, *, query: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    wait_message = "Please wait while I gather the top ten search results."
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    await ctx.channel.send(wait_message)
    results = ''
    for j in search(query, tld="co.in", lang='en', num=10, stop=10, pause=2):
        results += "<" + j + ">\n"

    await ctx.channel.send(f'{results}')


@bot.command(name='evaluate', help='evaluates line of code given')
async def evaluate(ctx, code: str):
    g3 = eval(code)
    await ctx.channel.send(f'{g3}')


@bot.command(name='solve', help='Solves any function given in Wolfram Format')
async def mathematica(ctx, function: str):
    evaluated = session.evaluate(function)
    await ctx.channel.send(f'```\n{evaluated}```')


@bot.command(name='translate', help='Translates a string to another language')
async def translate(ctx, user_input: str, trans_lang: str):
    translator = Translator()
    list_lang = googletrans.LANGCODES
    translations = translator.translate([user_input], dest=list_lang[trans_lang])
    for translation in translations:
        msg = translation.origin + ' ----> ' + translation.text
        error_msg = 'The section of text you want to translate makes the message over 2000 characters, '\
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
        await ctx.channel.send(f'{error_msg}')
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

bot.run(TOKEN)
