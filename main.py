import os
import discord
from discord.ext import commands
import mysql.connector
from dotenv import load_dotenv

description = '''m4x5ton Discord's best bot evr.'''

intents = discord.Intents.default()
intents.members = True

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

wipe_password = "boom"

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    

@bot.command()
async def create(ctx, name: str, discord_id = "0", ):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = db.cursor(buffered=True)

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()
    msg = ""

    if record is None:
        mysql_insert_query = """INSERT INTO teamkills (`name`, `discord_id`, `deaths`) 
                                VALUES (%s, %s, %s) """
        record = (name, discord_id, 0)
        cursor = db.cursor()
        cursor.execute(mysql_insert_query, record)
        msg = name + " added! Welcome to the Thunderdome."
    else:
        msg = "This guy already exists"

    await ctx.send(msg)
    
    db.commit()
    cursor.close()


@bot.command()
async def inject(ctx, injection_string: str):
    #Johnny Tables
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    injection_string = injection_string.replace("_", " ")

    print(injection_string)

    cursor = db.cursor(buffered=True)
    cursor.execute(injection_string)
    records = cursor.fetchall()
    msg = ""

    if records is not None:
        ##If statement returns results, print them out
        for row in records:
            for item in row:
                msg += str(item) + " "
            msg += "\n"

    if (msg == ""):
        msg = "Done!"

    await ctx.send(msg)
    db.commit()
    cursor.close()


@bot.command()
async def remove(ctx, name: str):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    cursor = db.cursor(buffered=True)

    sql_select_query = """DELETE FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))

    await ctx.send("OK - done")

    db.commit()
    cursor.close()


@bot.command()
async def add(ctx, name: str):
    """Adds TK`s"""
    # await ctx.message.delete()
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = db.cursor(buffered=True)

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()

    msg = ""

    if record is not None:

        print(record[3])
        sql_update_query = """UPDATE teamkills SET deaths = %s WHERE name = %s"""
        new_kill = record[3] + 1
        cursor.execute(sql_update_query, (new_kill, name))

        msg = "TK ADDED: \n" + name + " is now on " + str(new_kill) + " Kills"
    else:
        msg = "TK Failed: \n Name does not exist."
    
    await ctx.send(msg)

    db.commit()
    cursor.close()


@bot.command()
async def set(ctx, name: str, num: int):
    """Sets the score"""
    # await ctx.message.delete()
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = db.cursor(buffered=True)

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()

    msg = ""

    if record is not None:
        cursor = db.cursor(buffered=True)
        sql_select_query = """UPDATE teamkills SET deaths = %s WHERE name = %s"""
        cursor.execute(sql_select_query, (num, name))
        msg = "SCORE SET: \n" + name + " is now on " + str(num) + " Kills"
    else:
        msg = "Person doesn't exist, didn't do anything."
        pass

    await ctx.send(msg)

    db.commit()
    cursor.close()


@bot.command()
async def get(ctx, name: str):
    """f"""
    # await ctx.message.delete()
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s """
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchone()

    msg = ""

    if record is not None:
        msg = record[1] + " is on " + str(record[3]) + " kills."
    else:
        msg = "You numpty, " + name + " doesn't even exist. Use '$add " + name + "' to add them."
    
    await ctx.send(msg)

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
        database=db_database
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
async def wipe(ctx, password: str):
    """Wipe TK`s"""
    await ctx.message.delete()
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
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
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
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
    await ctx.send("What an absolute Nigel")


@bot.command()
async def winner(ctx):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    cursor = db.cursor()

    sql_select_query = """SELECT * FROM teamkills ORDER BY deaths desc LIMIT 1"""
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    if record is not None:
        msg = "As it looks, " + record[1] + " is in the lead with a smashing " + str(record[3]) + " teamkills."
    else:
        msg = "Nobody is here"

    await ctx.send(msg)
    cursor.close()


@bot.command()
async def what(ctx):
    """Help message"""
    await ctx.send("""
    Help:
    $create [name] [discord_id]: Creates a new player.
    $add [name]: Adds a teamkill to their tally.
    $check: Check the scoreboard.
    $rename [name] [new_name]: Mistyped their name? Fix your ways here.
    $set [name] [score]: Sets the score.
    $remove [name]: Removes that player.
    $winner: Try it and see
    
    Name and shame. NAME AND SHAME.""")

bot.run(os.getenv('BOT_TOKEN'))
