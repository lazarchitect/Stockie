import os
import discord
from dotenv import load_dotenv
import stock_api
from time import sleep
from discord.ext import tasks, commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')

#initial values will be populated here, probs should get saved in a DB
ticker_lists = {
    "eddie": ["SPY", "ACN"]
}

client = discord.Client()

@tasks.loop(seconds=86400)
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

            message1 = stock_api.get_time_series_daily(ticker)
            if message1 == "":
                message1 = "Error on ticker " + ticker + ": please verify that symbol exists and try again."
                await channel.send(message1)

            else:
                ticker_lists[channel_name].append(ticker)
                message = ticker + " added"
                print(message)
                await channel.send(message)

        elif command == "!remove":
            ticker = tokens[1]
            ticker_lists[channel_name].remove(ticker)
            message = ticker + " removed"
            print(message)
            await channel.send(message)

        elif command == "!get":
            ticker = tokens[1]
            message = stock_api.get_time_series_daily(ticker, delay=0)
            if message == "":
                message = "Error on ticker " + ticker + ": please verify that symbol exists and try again."
            await channel.send(message)

        elif command == "!help":
            message = """COMMANDS\n
                        *get* to retrieve a single ticker's daily data\n
                        *add* to add a specific ticker to the list for the channel\n
                        *remove* to remove a ticker from the list"""
            await channel.send(message)

client.run(DISCORD_TOKEN)
