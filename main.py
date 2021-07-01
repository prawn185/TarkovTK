import discord
from discord.ext import commands
import mysql.connector

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# put into env

# tarkov
# Killa69!


@bot.command()
async def create(ctx, name: str, discord_id: str, ):
    db = mysql.connector.connect(
        host="localhost",
        user="tarkov",
        password="Killa69!",
        database="Tarkov"
    )

    mysql_insert_query = """INSERT INTO teamkills (`name`, `discord_id`, `deaths`) 
                            VALUES (%s, %s, %s) """

    record = (name, discord_id, 0)

    cursor = db.cursor()

    cursor.execute(mysql_insert_query, record)
    db.commit()
    print(cursor.rowcount, "Record inserted successfully into teamkills table")
    cursor.close()

    await ctx.send(name + " Added!")


@bot.command()
async def add(ctx, name: str):
    """Adds TK`s"""
    # await ctx.message.delete()
    pinned = ""
    msg = "TK ADDED: \n"

    db = mysql.connector.connect(
        host="localhost",
        user="tarkov",
        password="Killa69!",
        database="Tarkov"
    )

    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()
    sql_update_query = """UPDATE teamkills SET deaths = %s WHERE name = %s"""
    newkill = (record[3] + 1, name)
    cursor.execute(sql_update_query, newkill)

    sql_select_query2 = """select * from teamkills where name = %s"""
    cursor.execute(sql_select_query2, (name,))
    updated = cursor.fetchone()

    await ctx.send("TK ADDED: \n"+name+" is now on "+str(updated[3])+" Kills")

    db.commit()

    cursor.close()


@bot.command()
async def check(ctx):
    """Counts TK`s"""
    # await ctx.message.delete()
    msg = "TeamKillers: \n"

    db = mysql.connector.connect(
        host="localhost",
        user="tarkov",
        password="Killa69!",
        database="Tarkov"
    )

    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    for row in records:
        msg += row[1]+": "+str(row[3])+"\n"

    await ctx.send(msg)

    db.commit()

    cursor.close()

@bot.command()
async def wipe(ctx):
    """Wipe TK`s"""
    # await ctx.message.delete()
    db = mysql.connector.connect(
        host="localhost",
        user="tarkov",
        password="Killa69!",
        database="Tarkov"
    )

    cursor = db.cursor()
    sql_update_query = """UPDATE teamkills SET deaths = 0"""

    cursor.execute(sql_update_query)

    db.commit()



    await ctx.send("WIPEEEEEEE")

    db.commit()

    cursor.close()


@bot.command()
async def what(ctx):
    """Wipe TK`s"""
    await ctx.send("\nHelp:\n Create: Creates a new user $create {Name} {DiscordID}\n Add: Adds a kill $add {Name}\n "
                   "Check: Check total $check")



bot.run('000000000')
