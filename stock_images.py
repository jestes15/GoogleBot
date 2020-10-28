stock = {
    'TSLA': 'https://www.bing.com/th?id=AMMS_27430035dc27b10b74a6cd2e7db7ce5a&w=110&h=11'
            '0&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'AAPL': 'https://www.bing.com/th?id=AMMS_8f141d39181840922518b6793ae00344&w=110&h=11'
            '0&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'NVDA': 'https://www.bing.com/th?id=AMMS_db14109810abd5181387bc1d0d8880bd&w=110&h=11'
            '0&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'GOOGL': 'https://www.bing.com/th?id=AMMS_8f9327db2597fa57d2f42b4a6c5a9855&w=110&h=11'
             '0&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'INTC': 'https://www.bing.com/th?id=AMMS_9bc91eacd60174953177c4171c6d49b6&w=110&h=110'
            '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'AMD': 'https://www.bing.com/th?id=AMMS_df0b03f8657f8eaad90c38e7cfd119ce&w=110&h=110'
           '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'MSFT':  'https://www.bing.com/th?id=AMMS_55082fbed2bbeb930e47f1d56056472a&w=110&h=110'
             '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'IBM': 'https://www.bing.com/th?id=AMMS_41da901be1b295dc42c72dadb9c0f67d&w=110&h=110'
           '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'LDOS': 'https://www.bing.com/th?id=AMMS_bee0154677c5e08c4413057e2efe4344&w=110&h=110'
            '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=1.5&pid=16.1',
    'F': 'https://www.bing.com/th?id=AMMS_77d56bf069a844cfc5992a70e0d1183b&w=110&h=110&c='
         '7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1',
    'FB': 'https://www.bing.com/th?id=AMMS_8ddf76a14a2e3ad3ba62b46d49a75a74&w=110&h=110&c='
          '7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1',
    'ORCL': 'https://www.bing.com/th?id=AMMS_299d4c720597f57a5478e2509e71722e&w=110&h=110'
            '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1',
    'TWTR': 'https://www.bing.com/th?id=AMMS_4021904fb0bf29ef3d1508bdabd240c1&w=110&h=110'
            '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1',
    'NFLX': 'https://www.bing.com/th?id=AMMS_8956da194d73a7f4a5c43144b83e4c42&w=110&h=110'
            '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1',
    'GE': 'https://www.bing.com/th?id=AMMS_8bf31de08fbbc2d36f87c39574105e53&w=110&h=110'
          '&c=7&rs=1&qlt=95&pcl=f9f9f9&cdv=1&dpr=2.5&pid=16.1'
}


def load_stock_img(symbol: str):
    url = stock[symbol]
    return url
