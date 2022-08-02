import os
from twitchio.ext import commands
import json

with open("data.json", "r") as f:
    data = json.load(f)

bot = commands.Bot(prefix='?', initial_channels=['lookatyourskill'], token=data["twitch"]["token"])

for filename in os.listdir('./extensions'):
    if filename.endswith('.py'):
        bot.load_module(f'extensions.{filename[:-3]}')
        print(f'Loaded {filename} Successful')


print("-----------------------------------------------------")

if __name__ == '__main__':
    bot.run()
