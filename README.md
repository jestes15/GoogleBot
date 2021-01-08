# GoogleBot
© by Joshua Estes 2020
This bot is made to do an assortment of tasks to help users within a discord server. Can do complex math powered by Wolfram Engine, can use Google and can look at stocks prices and other metrics, powered by Robinhood.

To install the discord bot, pull it onto a computer using `git clone https://github.com/jestes15/GoogleBot.git` and run the init script.

The following commands are only applicable to a Linux server.

`sudo apt update`

`sudo apt upgrade -y`

`sudp apt install nodejs -y`

`sudo apt install npm -y`

`sudo npm install forever -g`

`curl -o WolframEngine.sh https://files.wolframcdn.com/WolframEngine/12.1.1.0/WolframEngine_12.1.1_LINUX.sh?4ae6ee529e4e0d5967853f9964b23dfeb8566c7eb008cacb7094220e3cec0c49c591ac95f271470d926a3d920a6612c557164b74bee136637e21f6bd0ca760f3c2e8d2b79ec2eadf476c1d4a8efea0691d2efc087c4fae4740b47e7624b86326671970e41fLINUX_.sh`

`sudo bash WolframEngine.sh`

`wolframscript`

`git clone https://github.com/jestes15/GoogleBot.git`

`cd GoogleBot`

`chmod 700 init`

`./init`

`forever start -c python3 main.py`

If using a linux server put this into a file and run `chmod 700 <filename>` on the file. In order to use this bot, you will need a Dev license for Wolfram Engine.