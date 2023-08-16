#Imports
import discord
from discord.ext import commands, tasks
import random
from random import randint
from itertools import cycle
import os
import asyncio
import json

#changes server prefix
async def get_server_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]

#Variables
token = ""#< Input token here
client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())
bot_status = cycle(["Made by ", "Type >help in a new server"]) #< Input name here

#Loops
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#Events
@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is Ready!")
    change_status.start()

@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = ">"

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

#Slash Commands
@client.tree.command(name="ping", description="Shows bot latency in milliseconds")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"{bot_latency} ms.")

@client.tree.command(name="prefix", description="Sets the selected server's prefix")
async def prefix(ctx, *, newprefix: str):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

@client.tree.command(name="invite", description="Sends the bot's invite link")
async def invite(ctx):
    await ctx.send("Invite link: https://discord.com/api/oauth2/authorize?client_id=1140563849381150741&permissions=8&scope=bot")

#Functions
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(token)

asyncio.run(main())