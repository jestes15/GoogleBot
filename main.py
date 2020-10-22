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
import csv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')

robin.authentication.login(username, password)

bot = commands.Bot(command_prefix="Hey Google, ")

today = date.today()

session = WolframLanguageSession()
print(session)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')  # Sends an online message to the command line
    channel = bot.get_channel(756568695320608910)  # Gets the channel with this channel id
    await bot.change_presence(activity=discord.Game(name="search and record"))
    await channel.send(f'{bot.user.name} has connected to discord')
    # Sends an online message to the aforementioned channel


@bot.command(name='get', help='Takes stock symbol, returns price')
async def load_stock(ctx, option=None, stocks=None, str3=None, everything=None):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    if option != 'common':
        if option is None:
            msg = "Im sorry, but I need the symbol for the stock you are looking for, please try again. " \
                  "If you think I made a mistake, please contact <@!610469915442282526>  to resolve this issue"
            await ctx.channel.send(f'{msg}')

        elif stocks == 'description':
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
                msg = 'Price = $' + str(stock_info_number) + '\nP/B Ratio = ' + str(pb_ratio[0]) + '\nP/E Ratio = ' + \
                      str(pe_ratio[0]) + '\nDividend Yield = ' + str(dividend_yield[0])
                await ctx.channel.send(f'{msg}')

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
                sub += string[0:-1] + '\nPrice = $' + str(stock_price[0]) + '\nP/B Ratio = ' + str(pb_ratio[0])
                sub += '\nP/E Ratio = ' + str(pe_ratio[0]) + '\nDividend Yield = ' + str(dividend_yield[0]) + '\n'
                num += 1
            await ctx.channel.send(f'{sub}')

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
                sub += string[0:-1] + ' = $' + str(stock_price[0]) + '\n'
                num += 1
            await ctx.channel.send(f'{sub}')


@bot.command(name='add', help='Adds a symbol to the common stock list')
async def mutation(ctx, stock: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    with open("common-stock-list.txt", 'a') as f:
        f.write(stock + '\n')
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
async def show(ctx, encryption: str, choices: str):
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
async def encode(ctx, get_string: str, using: str, get_choice: str):
    encode_s = cmd.EncodeString
    encrypted_string = encode_s.switch(cmd.EncodeString(get_string), get_choice).string
    await ctx.channel.send(f'{encrypted_string}')


@bot.command(name='echo', help='Echos back user input')
async def echo(ctx, user_input: str):
    if 'gay' in user_input.lower():
        msg = "I'm sorry, that message is not allowed."
        await ctx.channel.send(f'{msg}')
    elif 'homo' in user_input.lower():
        msg = "I'm sorry, that message is not allowed."
        await ctx.channel.send(f'{msg}')
    elif 'fag' in user_input.lower():
        msg = "I'm sorry, that message is not allowed."
        await ctx.channel.send(f'{msg}')
    else:
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(f'{user_input}')


@bot.command(name='AddSaying')
async def add_saying(ctx, *, arg):
    await ctx.channel.send(f'{arg}')


@bot.command(name='announce', help='Allows announcement to be used')
async def ann(ctx, user_input: str, channel_id: int, delete=False):
    await ctx.channel.send("Request received: executing now")
    channel = bot.get_channel(channel_id)
    if delete is True:
        await channel.send(f'{user_input} {str(delete)}')
    else:
        await channel.send(f'{user_input}')
    # Echos user input


@bot.command(name='give', help='syntax: give me quotes. Sends a random meme statement')
async def meme(ctx, me: str, quotes: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    meme_dictionary = {
        1: 'Hello There',
        2: '*Nani*',
        3: 'Boi if you don\'t get that out of here',
        4: '*China*'
    }
    x = int(r.randint(1, 4))
    await ctx.channel.send(f'{meme_dictionary[x]}')

audio_dict = {
    1: 'playme.mp3',
    2: 'PlayMe2.mp3'
}


@bot.command(name='send', help='syntax: send me memes. Shows an image')
async def image(ctx, me: str, memes: str, type_f=None, choice=None):
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
    if type_f is not None:
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
            verse_line = 2 * (verse - 1)
            msg = bible_read[verse_line]
            await ctx.channel.send(f'{msg}')

        else:
            i = verse
            i_i = last_verse + 1
            bible_verse = ''
            while i < i_i:
                verse_line = 2 * (i - 1)
                bible_verse += bible_read[verse_line] + '\n'
                i += 1
            length = len(bible_verse)
            if length < 2001:
                await ctx.channel.send(f'{bible_verse}')
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
async def google(ctx, query: str):
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
async def translate(ctx, user_input: str, *, trans_lang: str):
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
            await ctx.channel.send(f'{msg}')


@bot.command(name='roll', help='Rolls a dice')
async def roll(ctx, dice_type: str):
    dice_type1 = dice_type.lower()
    num = int(dice_type1.replace("d", ""))
    result = r.randint(1, num)
    await ctx.channel.send(f'{result}')

bot.run(TOKEN)
