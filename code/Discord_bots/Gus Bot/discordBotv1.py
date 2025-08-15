import discord
from discord.ext import commands
from discord import app_commands
import praw
import random
from RedditDemo import find

DISCORD_TOKEN = "MTA1OTczNTcxODM5NTY1NDIyNA.GZIsAd.NkiGmpaY_-F5y1lIECcvdigOET_pBJZHWiYTCw"

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Gus Ready...")
    try:
        synced = await client.tree.sync()
        print("Synced {} command(s)".format(len(synced)))
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('.find '):
        msg = message.content[6:]
        try:
            results = find("".join(msg.split(" ")))
            await message.channel.send(random.choice(results))
        except:
            print("".join(msg.split(" ")))
            await message.channel.send("Cannot find {}".format(msg))

# @client.command()
# async def find(ctx, *args):
#     await ctx.channel.send(args)
#     try:
#         searchName  = "".join(args)
#         await ctx.channel.send(random.choice(find(searchName)))
#     except:
#         await ctx.channel.send("{} does not exist".format(args))

@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("what a dooo")


@client.tree.command(name="say", description="Message to say", guild=discord.Object(id=825505585193680916))
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(thing_to_say)


client.run(DISCORD_TOKEN)