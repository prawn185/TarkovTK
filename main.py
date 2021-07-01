import discord
from discord.ext import commands
import mysql.connector

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

db_host = "localhost"
db_user = "tarkov"
db_password = "Killa69!"
db_name = "Tarkov"

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
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    mysql_insert_query = """INSERT INTO teamkills (`name`, `discord_id`, `deaths`) 
                            VALUES (%s, %s, %s) """

    record = (name, discord_id, 0)

    cursor = db.cursor()

    cursor.execute(mysql_insert_query, record)
    db.commit()
    print(cursor.rowcount, "Record inserted successfully into teamkills table")
    cursor.close()

    await ctx.send(name + " added! Welcome to the Thunderdome.")


@bot.command()
async def add(ctx, name: str):
    """Adds TK`s"""
    # await ctx.message.delete()
    pinned = ""
    msg = "TK ADDED: \n"

    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()
    sql_update_query = """UPDATE teamkills SET deaths = %s WHERE name = %s"""
    new_kill = (record[3] + 1, name)
    cursor.execute(sql_update_query, new_kill)

    sql_select_query2 = """select * from teamkills where name = %s"""
    cursor.execute(sql_select_query2, (name,))
    updated = cursor.fetchone()

    await ctx.send("TK ADDED: \n" + name + " is now on " + str(updated[3]) + " Kills")

    db.commit()
    cursor.close()


@bot.command()
async def check(ctx):
    """Counts TK`s"""
    # await ctx.message.delete()
    msg = "TeamKillers: \n"

    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
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
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()
    sql_update_query = """UPDATE teamkills SET deaths = 0"""
    cursor.execute(sql_update_query)

    await ctx.send("WIPEEEEEEE")

    db.commit()
    cursor.close()


@bot.command()
async def rename(ctx, name: str, new_name: str):
    """Renames somebody"""
    # await ctx.message.delete()

    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()

    if record is not None:
        sql_update_query = """UPDATE teamkills SET name = %s WHERE name = %s"""
        name_tuple = (name, new_name)
        cursor.execute(sql_update_query, name_tuple)
        await ctx.send("RENAMED: \n" + name + " is now called " + new_name + ".")
    else:
        await ctx.send("You numpty, " + name + " doesn't even exist. Use '$add + " + name + "' to add them.")
    
    db.commit()
    cursor.close()

@bot.command()
async def nigel(ctx):
    """Absolutely thrashes someone"""
    # await ctx.message.delete()
    await ctx.send("What an absolute Nigel.")

@bot.command()
async def what(ctx):
    """Wipe TK`s"""
    await ctx.send("""
    Help:
    $create [name] [discord_id]: Creates a new user.
    $add [name]: Adds a teamkill to their tally.
    $check: Check the scoreboard.
    $rename [name] [new_name]: Mistyped their name? Fix your ways here.
    
    Name and shame. NAME AND SHAME.""")

bot.run('000000000')
