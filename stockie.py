import os
import discord
from dotenv import load_dotenv
import stock_api
from time import sleep
from discord.ext import tasks, commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
#CHANNEL_NAME = os.getenv('CHANNEL_NAME')

ticker_lists = {
    "eddie": []
}

client = discord.Client()

@tasks.loop(seconds=10)
async def create_loop():

    for channel_name in list(ticker_lists.keys()):
        guild = discord.utils.get(client.guilds, name=GUILD_NAME)
        channel = discord.utils.get(guild.channels, name=channel_name)

        message = stock_api.get_stock_data(ticker_lists[channel_name])

        if message == "":
            continue

        await channel.send(message)

@client.event
async def on_ready():
    print("stockie is ready")
    create_loop.start()

@client.event
async def on_message(message):
    if(message.content[0] == "!"):

        channel = message.channel
        channel_name = channel.name
        tokens = message.content.split(" ")
        command = tokens[0]

        if command == "!add":
            ticker = tokens[1]
            ticker_lists[channel_name].append(ticker)
            print(ticker + " added to list " + channel_name)

        elif command == "!remove":
            ticker = tokens[1]
            ticker_lists[channel_name].remove(ticker)
            print(ticker + " removed from list " + channel_name)

client.run(DISCORD_TOKEN)
