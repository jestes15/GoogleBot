from datetime import date
import datetime
from discord.ext import commands
import discord
from dotenv import load_dotenv
import encryption_cmd as cmd
from googlesearch import search
import logging
import os
import random as r
import robin_stocks as robin
from wolframclient.evaluation import WolframLanguageSession

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')

robin.authentication.login(username, password)

bot = commands.Bot(command_prefix="Hey Google, ")

today = date.today()

LOG = os.getcwd() + "/tmp/ccd.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)

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
            await ctx.channel.send(msg)

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
                await ctx.channel.send(msg)
            else:
                stock_info_number = stock_info[0]
                await ctx.channel.send('Price = $' + str(stock_info_number) + '\nP/B Ratio = ' + str(pb_ratio[0]) +
                                       '\nP/E Ratio = ' + str(pe_ratio[0]) + '\nDividend Yield = ' +
                                       str(dividend_yield[0]))

    if option == 'common':
        if everything == 'everything':
            stock_list2 = {}
            stock_list = []
            j = 0
            with open('common-stock-list.txt', 'r') as f:
                array = f.readlines()
            for row in array:
                stock_list.append(row)
                j += 1
            current_date = datetime.datetime.now()
            d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
            stock_list2[0] = d2

            await ctx.channel.send("Please wait while I compile the information you have "
                                   "requested, approximately 2 to 3 seconds")
            await discord.channel.TextChannel.trigger_typing(self=ctx)
            num = 0
            sub = stock_list2[0] + '\n'
            while num < (len(array)):
                string = array[num]
                stock_price = robin.stocks.get_latest_price(array[num])
                pb_ratio = robin.stocks.get_fundamentals(array[num], 'pb_ratio')
                pe_ratio = robin.stocks.get_fundamentals(array[num], 'pe_ratio')
                dividend_yield = robin.stocks.get_fundamentals(array[num], 'dividend_yield')
                sub += string[0:-1] + '\nPrice = $' + str(stock_price[0]) + '\nP/B Ratio = ' + str(pb_ratio[0])
                sub += '\nP/E Ratio = ' + str(pe_ratio[0]) + '\nDividend Yield = ' + str(dividend_yield[0]) + '\n'
                num += 1
            await ctx.channel.send(sub)

        else:
            stock_list2 = {}
            stock_list = []
            j = 0
            with open('common-stock-list.txt', 'r') as f:
                array = f.readlines()
            for row in array:
                stock_list.append(row)
                j += 1
            current_date = datetime.datetime.now()
            d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
            stock_list2[0] = d2

            await ctx.channel.send("Please wait while I compile the information you have requested, approximately 2 "
                                   "to 3 seconds")
            await discord.channel.TextChannel.trigger_typing(self=ctx)
            num = 0
            sub = stock_list2[0] + '\n'
            while num < (len(array)):
                string = array[num]
                stock_price = robin.stocks.get_latest_price(array[num])
                sub += string[0:-1] + ' = $' + str(stock_price[0]) + '\n'
                num += 1
            await ctx.channel.send(sub)


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
    if message.author == bot.user:
        quote = "bruh"
    else:
        quote = 'Hello mad lad'
    await message.channel.send(quote)
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
    await ctx.channel.send("When using the encode command, choices are case sensitive.\n" + choices)


@bot.command(name='encode', help='syntax: encode <String> using <choice of encryption>')
async def encode(ctx, get_string: str, using: str, get_choice: str):
    encode_s = cmd.EncodeString
    encrypted_string = encode_s.switch(cmd.EncodeString(get_string), get_choice).string
    await ctx.channel.send(encrypted_string)


@bot.command(name='echo', help='Echos back user input')
async def echo(ctx, user_input: str):
    if 'gay' in user_input.lower():
        await ctx.channel.send("I'm sorry, that message is not allowed.")
    else:
        await discord.channel.TextChannel.trigger_typing(self=ctx)
        await ctx.channel.send(user_input)


@bot.command(name='announce', help='Allows announcement to be used')
async def ann(ctx, user_input: str, channel_id: int, delete=False):
    await ctx.channel.send("Request received: executing now")
    channel = bot.get_channel(channel_id)
    if delete is True:
        await channel.send(user_input + ' ' + str(delete))
    else:
        await channel.send(user_input)
    # Echos user input


@bot.command(name='give', help='syntax: give me quotes. Sends a random meme statement')
async def meme(ctx, me: str, quotes: str):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    meme_dictionary = {
        1: 'Hello There',
        2: '*Nani*',
        3: 'Boi if you don\'t get that out of here',
        4: '*China*',
        5: 'Trump 2020',
        6: '*Trump 2020*',
        7: '||Trump 2020||'
    }
    x = int(r.randint(1, 7))
    await ctx.channel.send(meme_dictionary[x])


@bot.command(name='send', help='syntax: send me memes. Shows an image')
async def image(ctx, me: str, memes: str, type_f=None):
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
            await ctx.channel.send(file=discord.File('Audio/playme.mp3'))
        if type_f == 'gif':
            await ctx.channel.send(file=discord.File('GIF/258c8822b6a11bdc8d0060bd9bb47df3.gif'))
    else:
        x1 = str(r.randint(6, 16))
        await ctx.channel.send(file=discord.File('Images/image' + x1 + '.jpg'))


@bot.command(name='search', help='syntax=<book><chapter><start-verse><optional: end-verse>')
async def GetBibleVerse(ctx, for2: str, book_name: str, chapter: int, verse: int, last_verse=0):
    await discord.channel.TextChannel.trigger_typing(self=ctx)
    location = 'Bible/' + book_name + '/' + book_name + '_' + str(chapter) + '.txt'
    with open(location, 'r') as bible:
        bible_read = bible.readlines()

        if last_verse == 0:
            verse_line = 2 * (verse - 1)
            await ctx.channel.send(bible_read[verse_line])

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
                await ctx.channel.send(bible_verse)
            else:
                msg = "Error: You have requested too many Bible verses " \
                      "and have exceeded the discord limit of 2000 characters " \
                      "please shorten your request and try again."
                await ctx.channel.send(msg)


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

    await ctx.channel.send(results)


@bot.command(name='evaluate', help='evaluates line of code given')
async def evaluate(ctx, code: str):
    g3 = eval(code)
    await ctx.channel.send(g3)


@bot.command(name='solve', help='testing')
async def mathematica(ctx, function: str):
    evaluated = session.evaluate(function)
    await ctx.channel.send('```\n' + str(evaluated) + '```')

bot.run(TOKEN)
