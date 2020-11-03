msg = 'hello'


class LoadStock:
    def __init__(self, option_2=None, stocks=None, crypto_modifier=None, everything=None):
        self.option = option_2
        self.stocks = stocks
        self.crypto_modifier = crypto_modifier
        self.description = everything

    def common(self):
        title = 'Common Stocks'
        array = [title, self.option]
        return array

    def common_everything(self):
        print(msg)

    def crypto(self):
        print(msg)

    def crypto_value(self):
        print(msg)

    def crypto_modifier(self):
        print(msg)

    def stock(self):
        print(msg)

    def stock_description(self):
        print(msg)
