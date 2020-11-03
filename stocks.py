class LoadStock:
    def __init__(self, option=None, stocks=None, crypto_modifier=None, everything=None):
        self.option = option
        self.stocks = stocks
        self.crypto_modifier = crypto_modifier
        self.description = everything

    def decision(self):
        default = 'Not available'
        name = ''
        if self.option == 'common':
            if self.description == 'everything':
                name = 'common_everything'
            else:
                name = 'common'
        elif self.option == 'crypto':
            if self.crypto_modifier is None:
                name = 'crypto_value'
            else:
                name = 'crypto'


            return getattr(self, name, lambda: default)()

    def common(self):

    def common_everything(self):

    def crypto(self):
        current_price = f'The current price of {stocks} is ${crypto_value}'
        embed_var = discord.Embed(title=f'{"Cryptocurrency"}', description=current_price, color=0x00b300)
        embed_var.set_thumbnail(url='https://th.bing.com/th/id/OIP.Y25UPylA8mnk-SfKSnEEGQHaFb?pid=Api&rs=1')
        await ctx.channel.send(embed=embed_var)
        
    def crypto_value(self):

    def crypto_modifier(self):

    def stock(self):

    def stock_description(self):

