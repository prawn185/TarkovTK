import os
import discord

import asyncio
import youtube_dl

from discord.ext import commands

import aiomysql  # async db

from dotenv import load_dotenv

description = '''Shaun & Sean's Mechanized Commander'''

intents = discord.Intents.default()
intents.members = True

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')
db_admin_whitelist = [str(i) for i in os.environ.get(
    "DB_ADMIN_WHITELIST").split(",")]

wipe_password = "boom"

bot = commands.Bot(command_prefix='!',
                   description=description, intents=intents)


@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def printout(ctx):
    """Check that it works"""
    # ctx (context) object
    # details available at https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#context
    #   https://discordpy.readthedocs.io/en/stable/api.html#guild
    #   https://discordpy.readthedocs.io/en/stable/api.html#message
    print("It works!")
    await ctx.send("It works!")
    # await ctx.send(ctx.message.guild)
    await ctx.send(ctx.message.guild.id)


@bot.command()
async def create(ctx, name: str, discord_id="0", ):
    conn = await aiomysql.connect(

        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))
    record = await cursor.fetchone()
    msg = ""

    if record is None:
        mysql_insert_query = """INSERT INTO teamkills (`name`, `discord_id`, `deaths`, `guild_id`)
                                VALUES (%s, %s, %s, %s) """
        await cursor.execute(mysql_insert_query, (name, discord_id, 0, ctx.message.guild.id))
        msg = name + " added! Welcome to the Thunderdome."
    else:
        msg = "This guy already exists"

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def inject(ctx, injection_string: str):
    # Johnny Tables

    conn = await aiomysql.connect(

        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    if not (str(ctx.message.author.id) in db_admin_whitelist):
        print("Invalid user - Injection command cancelled.")
        return

    print("We're about to inject:\n" + injection_string)

    await cursor.execute(injection_string)
    records = await cursor.fetchall()
    msg = ""

    if records is not None:
        # If statement returns results, print them out
        for row in records:
            for item in row:
                msg += str(item) + " "
            msg += "\n"

    if (msg == ""):
        msg = "Done!"

    await ctx.send(msg)
    await conn.commit()
    await cursor.close()


@bot.command()
async def remove(ctx, name: str):
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """DELETE FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))

    await ctx.send("OK - done")

    await conn.commit()
    await cursor.close()


@bot.command()
async def add(ctx, name: str):
    """Adds TK`s"""
    # await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))
    record = await cursor.fetchone()

    msg = ""

    if record is not None:
        sql_update_query = """UPDATE teamkills SET deaths = %s WHERE name = %s AND guild_id = %s"""
        new_kill = record[3] + 1
        await cursor.execute(sql_update_query, (new_kill, name, ctx.message.guild.id))

        msg = "TK ADDED: \n" + name + " is now on " + str(new_kill) + " Kills"
    else:
        mysql_insert_query = """INSERT INTO teamkills (`name`, `deaths`, `guild_id`)
                                VALUES (%s, %s, %s) """
        await cursor.execute(mysql_insert_query, (name, 0, ctx.message.guild.id))
        msg = name + " does not exist, added instead! Welcome to the Thunderdome."

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def set(ctx, name: str, num: int):
    """Sets the score"""
    # await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))
    record = await cursor.fetchone()

    msg = ""

    if record is not None:
        sql_select_query = """UPDATE teamkills SET deaths = %s WHERE name = %s AND guild_id = %s"""
        await cursor.execute(sql_select_query, (num, name, ctx.message.guild.id))
        msg = "SCORE SET: \n" + name + " is now on " + str(num) + " Kills"
    else:
        msg = "Person doesn't exist, didn't do anything."
        pass

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def get(ctx, name: str):
    """f"""
    # await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))
    record = await cursor.fetchone()

    msg = ""

    if record is not None:
        msg = record[1] + " is on " + str(record[3]) + " kills."
    else:

        msg = "You numpty, " + name + \
              " doesn't even exist. Use '!add " + name + "' to add them."

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def check(ctx):
    """Counts TK`s"""
    # await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills where guild_id = %s ORDER BY deaths DESC"""
    await cursor.execute(sql_select_query, (ctx.message.guild.id,))
    records = await cursor.fetchall()
    print("Fetching teamkillers list")
    msg = "TeamKillers: \n"
    for row in records:
        msg += row[1] + ": " + str(row[3]) + "\n"

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def wipe(ctx, password: str):
    """Wipe TK`s"""
    await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()
    sql_update_query = """UPDATE teamkills SET deaths = 0 WHERE guild_id = %s"""

    msg = ""

    if password == wipe_password:

        await cursor.execute(sql_update_query, (ctx.message.guild.id,))

        msg = "WIPEEEEEEED"
    else:
        msg = "Password incorrect - You'll need it to perform a wipe."
        pass

    await ctx.send(msg)

    await conn.commit()
    await cursor.close()


@bot.command()
async def rename(ctx, name: str, new_name: str):
    """Renames somebody"""
    # await ctx.message.delete()
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE name = %s AND guild_id = %s"""
    await cursor.execute(sql_select_query, (name, ctx.message.guild.id))
    record = await cursor.fetchone()

    if record is not None:
        sql_update_query = """UPDATE teamkills SET name = %s WHERE name = %s AND guild_id = %s"""
        await cursor.execute(sql_update_query, (new_name, name, ctx.message.guild.id))
        await ctx.send("RENAMED: \n" + name + " is now called " + new_name + ".")
    else:

        await ctx.send("You numpty, " + name + " doesn't even exist. Use '!add " + name + "' to add them.")

    await conn.commit()
    await cursor.close()


@bot.command()
async def nigel(ctx):
    """Absolutely thrashes someone"""
    # await ctx.message.delete()
    await ctx.send("What an absolute Nigel")


@bot.command()
async def winner(ctx):
    conn = await aiomysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_database,
    )
    cursor = await conn.cursor()

    sql_select_query = """SELECT * FROM teamkills WHERE guild_id = %s ORDER BY deaths desc LIMIT 1"""
    await cursor.execute(sql_select_query, (ctx.message.guild.id,))
    record = await cursor.fetchone()
    if record is not None:
        msg = "As it looks, " + \
              record[1] + " is in the lead with a smashing " + \
              str(record[3]) + " teamkills."
    else:
        msg = "Nobody is here"

    await ctx.send(msg)
    await cursor.close()


@bot.command()
async def what(ctx):
    """Help message"""
    await ctx.send("""
    Help:

    !create [name] [discord_id]: Creates a new player.
    !add [name]: Adds a teamkill to their tally.
    !check: Check the scoreboard.
    !rename [name] [new_name]: Mistyped their name? Fix your ways here.
    !set [name] [score]: Sets the score.
    !remove [name]: Removes that player.
    !winner: Try it and see.

    Name and shame. NAME AND SHAME.""")


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',

    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'

}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # @commands.command()
    # async def play(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stimpy(self, ctx, *, url=""):
        """Streams from a url (same as yt, but doesn't predownload)"""
        url = "https://youtu.be/IZui2PYfTSk"
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @stimpy.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")

                raise commands.CommandError(
                    "Author not connected to a voice channel.")

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot.add_cog(Music(bot))

bot.run(os.getenv('BOT_TOKEN'))
