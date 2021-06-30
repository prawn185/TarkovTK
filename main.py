import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/tk', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


users = [
    ['Max', 0],
    ['Prawn', 0],
    ['Smizzle', 0],
    ['Snuggles', 0],
    ['Mona', 0],
    ['Panda', 0],
    ['Hedwig', 0],
    ['Geo', 0]
]


@bot.command()
async def add(ctx, name: str):
    """Counts TK's"""

    pinned = ""
    msg = "Team Kills: "

    # Get pinned message

    # Read Pinned Msg

    # /tkadd name
    #pluses 1 to the message
    #edit the pinned msg

    # ctx.channel.purge(1)

    # sticky = await ctx.send(msg)

    # pinned = await ctx.pins()
    stick = ctx.pins()
    print(await stick)
    print(await stick.content())
    # sticky = await sticky.channel.get_message(int(859939382814179339))
    # # await sticky.pin()





bot.run('ODU5OTA1MTg5ODA3OTE1MDQ4.YNzfHQ.2SJ2JJnSdUOV9TzOhyoAKG94wLA')
