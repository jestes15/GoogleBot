import robin_stocks as robin
import datetime
import stock_images as si

msg = 'hello'
Discord_ID = '<@!610469915442282526> or DarthBane#8863'


class LoadStock:
    def __init__(self, option=None, stocks=None, crypto_modifier=None, everything=None):
        self.option = option
        self.stocks = stocks
        self.crypto_modifier = crypto_modifier
        self.description = everything

    @staticmethod
    def common():
        stock_list = {}
        with open('../GoogleBot-Cogs/common-stock-list.txt', 'r') as f:
            array = f.readlines()
        current_date = datetime.datetime.now()
        d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
        stock_list[0] = d2
        num = 0
        sub = stock_list[0] + '\n'
        while num < (len(array)):
            string = array[num]
            stock_price = robin.stocks.get_latest_price(array[num])
            sub += f'{string[0:-1]} = ${str(stock_price[0])}\n'
            num += 1
        title = 'Common Stocks'
        color = 0x00ff00
        array = [title, sub, color]
        return array

    @staticmethod
    def common_everything():
        stock_list = {}
        with open('../GoogleBot-Cogs/common-stock-list.txt', 'r') as f:
            array = f.readlines()
        current_date = datetime.datetime.now()
        d2 = current_date.strftime("%m/%d/%Y %I:%M:%S %p\n")
        stock_list[0] = d2
        num = 0
        sub = stock_list[0] + '\n'
        while num < (len(array)):
            string = array[num]
            stock_price = robin.stocks.get_latest_price(array[num])
            pb_ratio = robin.stocks.get_fundamentals(array[num], 'pb_ratio')
            pe_ratio = robin.stocks.get_fundamentals(array[num], 'pe_ratio')
            dividend_yield = robin.stocks.get_fundamentals(array[num], 'dividend_yield')
            sub += f'{string[0:-1]}\nPrice = ${stock_price[0]}\nP/B Ratio = {pb_ratio[0]}\nP/E Ratio = ' \
                   f'{pe_ratio[0]}\nDividend Yield = {dividend_yield[0]}\n\n'
            num += 1
        title = 'Common Stocks'
        color = 0x00ff00
        array = [title, sub, color]
        return array

    def crypto(self):
        crypto_value = robin.crypto.get_crypto_quote(self.stocks, 'mark_price')
        if crypto_value is None:
            error_msg = 'I\'m sorry, but the stock you are looking for is not here, make sure you ' \
                        'are using the correct Id and try again. If you can not figure it out, contact ' \
                        f'the dev of this bot, {Discord_ID}'
            title = 'Uh oh, an error has occurred'
            color = 0xff0000
            array = [title, error_msg, color]
            return array
        else:
            title = 'Cryptocurrency'
            current_price = f'The {self.crypto_modifier} of {self.stocks} is {crypto_value}'
            color = 0x00ff00
            url = 'https://th.bing.com/th/id/OIP.Y25UPylA8mnk-SfKSnEEGQHaFb?pid=Api&rs=1'
            array = [title, current_price, color, url]
            return array

    def crypto_modifier(self):
        crypto_value = robin.crypto.get_crypto_quote(self.stocks, self.crypto_modifier)
        if crypto_value is None:
            error_msg = 'I\'m sorry, but the stock you are looking for is not here, make sure you ' \
                        'are using the correct Id and try again. If you can not figure it out, contact ' \
                        f'the dev of this bot, {Discord_ID}'
            title = 'Uh oh, an error has occurred'
            color = 0xff0000
            array = [title, error_msg, color]
        else:
            title = f'{self.stocks}'
            current_price = f'The {self.crypto_modifier} of {self.stocks} is {crypto_value}'
            color = 0x00ff00
            url = 'https://th.bing.com/th/id/OIP.Y25UPylA8mnk-SfKSnEEGQHaFb?pid=Api&rs=1'
            array = [title, current_price, color, url]
        return array

    def stock(self):
        stock_info = robin.stocks.get_latest_price(self.option)
        pb_ratio = robin.stocks.get_fundamentals(self.option, 'pb_ratio')
        pe_ratio = robin.stocks.get_fundamentals(self.option, 'pe_ratio')
        dividend_yield = robin.stocks.get_fundamentals(self.option, 'dividend_yield')
        if stock_info[0] is None:
            title = 'uh oh, an error has occurred'
            error_msg = f"Im sorry, but the stock you are looking for is not in the archives. " \
                        f"If you think I made a mistake, please contact {Discord_ID} to resolve this issue"
            color = 0xff0000
            array = [title, error_msg, color]
        else:
            stock_info_number = stock_info[0]
            ret_msg = f'Price = ${stock_info_number}\nP/B Ratio = {pb_ratio[0]}\nP/E Ratio = {pe_ratio[0]}\n' \
                      f'Dividend Yield = {dividend_yield[0]}'
            title = f'{self.option}'
            color = 0x00ff00
            url = si.load_stock_img(self.option)
            if url is None:
                array = [title, ret_msg, color]
            else:
                array = [title, ret_msg, color, url]

        return array

    def stock_description(self):
        description = robin.stocks.get_fundamentals(self.option, 'description')
        title = f'{self.option}'
        color = 0x00ff00
        url = si.load_stock_img(self.option)
        if url is None:
            array = [title, description[0], color]
        else:
            array = [title, description[0], color, url]
        return array
