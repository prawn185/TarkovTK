import os
import discord
from discord.ext import commands
import mysql.connector
from dotenv import load_dotenv
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')


wipe_password = "boom"

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def create(ctx, name: str, discord_id: str, ):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    mysql_insert_query = """INSERT INTO teamkills (`name`, `discord_id`, `deaths`) 
                            VALUES (%s, %s, %s) """
    record = (name, discord_id, 0)
    cursor = db.cursor()
    cursor.execute(mysql_insert_query, record)

    await ctx.send(name + " added! Welcome to the Thunderdome.")
    
    db.commit()
    cursor.close()


@bot.command()
async def add(ctx, name: str):
    """Adds TK`s"""
    # await ctx.message.delete()
    pinned = ""
    msg = "TK ADDED: \n"

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()
    sql_update_query = """UPDATE teamkills SET deaths = %s WHERE name = %s"""
    new_kill = (record["kills"] + 1, name)
    cursor.execute(sql_update_query, new_kill)

    sql_select_query2 = """select * from teamkills where name = %s"""
    cursor.execute(sql_select_query2, (name,))
    updated = cursor.fetchone()

    await ctx.send("TK ADDED: \n" + name + " is now on " + str(updated["kills"]) + " Kills")

    db.commit()
    cursor.close()


@bot.command()
async def check(ctx):
    """Counts TK`s"""
    # await ctx.message.delete()
    msg = "TeamKillers: \n"

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    for row in records:
        msg += row["name"]+": "+str(row["kills"])+"\n"
        
    await ctx.send(msg)

    db.commit()
    cursor.close()


@bot.command()
async def wipe(ctx, password: str):
    """Wipe TK`s"""
    # await ctx.message.delete()
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = db.cursor()
    sql_update_query = """UPDATE teamkills SET deaths = 0"""

    msg = ""

    if (password == wipe_password):
        cursor.execute(sql_update_query)
        msg = "WIPEEEEEEE"
    else:
        msg = "Password incorrect - You'll need it to perform a wipe."
        pass

    await ctx.send(msg)

    db.commit()
    cursor.close()


@bot.command()
async def rename(ctx, name: str, new_name: str):
    """Renames somebody"""
    # await ctx.message.delete()

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s """
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()

    if record is not None:
        sql_update_query = """UPDATE teamkills SET name = %s WHERE name = %s"""
        name_tuple = (new_name, name)
        cursor.execute(sql_update_query, name_tuple)
        await ctx.send("RENAMED: \n" + name + " is now called " + new_name + ".")
    else:
        await ctx.send("You numpty, " + name + " doesn't even exist. Use '$add " + name + "' to add them.")
    
    db.commit()
    cursor.close()

@bot.command()
async def nigel(ctx):
    """Absolutely thrashes someone"""
    # await ctx.message.delete()
    await ctx.send(test_function())

def test_function():
    return "What an absolute Nigel"

@bot.command()
async def winner(ctx):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print(86125)
    cursor = db.cursor()

    sql_select_query = """SELECT TOP 1 FROM teamkills ORDER BY deaths desc"""
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    if record is not None:
        msg = "As it looks, " + record["name"] + " is in the lead with a smashing " + record["kills"] + " teamkills."
    else:
        msg = "Nobody is here"

    await ctx.send(msg)
    cursor.close()

@bot.command()
async def what(ctx):
    """Help message"""
    await ctx.send("""
    Help:
    $create [name] [discord_id]: Creates a new user.
    $add [name]: Adds a teamkill to their tally.
    $check: Check the scoreboard.
    $rename [name] [new_name]: Mistyped their name? Fix your ways here.
    
    Name and shame. NAME AND SHAME.""")

bot.run(os.getenv('BOT_TOKEN'))
