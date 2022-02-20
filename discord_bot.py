import backgroundstuff
import discord
from discord.ext import commands
import random
import logging
import asyncio
from my_queue import Queue

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.INFO)
description = '''Ein super toller Bot der tolle Sachen machen kann!'''
bot = commands.Bot(command_prefix='?', description=description)
bot.remove_command('help')
status = backgroundstuff.get_config("status")
channel_queues = []

bot.load_extension("cogs.chatcog")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logging.info("--- Bot ready ---")
    
# Eventgesteuerte Funktionen starten
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    
    if before.channel is None and after.channel is not None:
        await asyncio.sleep(0.5)
        await voice_events("welcome", member)
        await bot.change_presence(activity=discord.Game(random.choice(status))) # ändert den Status des Bots
    elif after.self_deaf:
        await voice_events("deaf", member)
    elif after.self_stream:
        await voice_events("stream", member)
    else: return

# reagiert auf Events in Voicechanneln
async def voice_events(pEvent, member):
    username = str(member)[:-5]
    channel = member.voice.channel
    channel_name = channel.name
    logging.info(f"{pEvent} triggered for {username}")

    file = backgroundstuff.generate_text(usecase=pEvent, u=username)

    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)


'''
AB HIER SIND DIE COMMANDS
'''

# Sagt das Wetter für den angegebenen Ort
@bot.command(brief="Aktuelles Wetter", description="Günni kommt in deinen Voicechannel und sagt das Wetter für den angegebenen Ort.\n Verwendung: ?wetter *STADT*")
async def wetter(ctx, *args):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    city = ' '.join(args)
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    async with ctx.channel.typing():
        file = backgroundstuff.weather_message(city)

        if file is None:
            await ctx.send("Etwas ist schief gelaufen :(")
            await ctx.send("Sicher, dass es diese Stadt gibt und du dich nicht verschrieben hast?")
            return

        channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Sagt einen zufälligen Fakt
@bot.command(brief='Sagt einen Fakt',description='Günni kommt in deinen Channel und sagt einen zufälligen Fakt.\n Nichts weiter zu beachten :)')
async def fakt(ctx):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author

    file = backgroundstuff.generate_text("fact")
    if file is None:
        await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")
        return

    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Sagt die Uhrzeit
@bot.command(brief='Uhrzeit', description="Sagt die aktuelle Uhrzeit.")
async def uhrzeit(ctx):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author

    file = backgroundstuff.get_uhrzeit()
    if file is None:
        await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")
        return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Beleidigt jemanden
@bot.command(brief='Kann Leute beleidigen.', description="Kommt zu dir und beleidigt die angegebene Person.\n Verwendung: ?beleidige *Name*")
async def beleidige(ctx, *args):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    target = ' '.join(args)
    origin = str(member)[:-5]

    file = backgroundstuff.generate_text("insult", t=target, o=origin)
    if file is None:
        await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")
        return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Erzählt einen Witz
@bot.command(brief='Erzählt einen Witz', description="Kommt zu dir und erzählt einen Witz")
async def witz(ctx):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author

    file = backgroundstuff.generate_text("joke")
    if file is None:
        await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")
        logging.warning("Error in 'witz'. File is None")
        return

    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Sagt was nettes
@bot.command(brief='Kann Leute mögen.', description="Kommt zu dir und sagt, dass du die angegebene Person magst. \n Voll auf liebe und so :) \n Verwendung: ?sendeLiebe *Name*")
async def sendeLiebe(ctx, *args):
    if ctx.message.author.voice is None:
        await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
        return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    target = ' '.join(args)
    origin = str(member)[:-5]

    file = backgroundstuff.generate_text("love", t=target, o=origin)
    if file is None:
        await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")
        logging.warning("Error in 'sendeLiebe'. File is None")
        return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Löscht Nachrichten in einem Channel
@bot.command(hidden=True, pass_context = True, brief="Löscht Nachrichten im Channel", description="Löscht standardmäßig 5 Nachrichten, mehr, wenn mehr angegeben wird.")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

'''
@client.command(hidden = True)
async def ping(ctx):
    logging.info("Ping!")
    await ctx.send('Pong! Ping beträgt: {0}ms'.format(round(client.latency, 1)))
'''

# Verbindet mit einem Channel, wenn es möglich ist
async def connect_when_possible(member):
    member_voice = member.voice.channel
    server = member.guild

    if not server.voice_client is None:
        return

    await member_voice.connect()
    logging.debug("Bot connected")

# Spielt files aus der Queue ab
async def queue_abspielen(member):
    await connect_when_possible(member)

    server = member.guild
    voice_connection = server.voice_client # Needs existing connection to work!
    
    channel_name = member.voice.channel.name
    queue_index = get_channel_queue_pos(channel_name)

    while True:
        await connect_when_possible(member)
        datei = channel_queue_dequeue(queue_index) + ".mp3"
        logging.debug("f{datei} wurde aus queue gelöscht")
        voice_connection.play(discord.FFmpegPCMAudio(str(datei)))
        logging.info(f"Now playing {datei}")
        while voice_connection.is_playing():
            pass
        channel_queues[queue_index].done()
        backgroundstuff.delete_file(datei)

        await voice_connection.disconnect()
        voice_connection.cleanup() 

        if channel_queues[queue_index].isEmpty():
            logging.debug("Queue is empty. Bot has disconnected.")
            return
        logging.debug("Queue not empty. Bot is playing next file")


def get_channel_queue_pos(channel_name):
	for queue in channel_queues:
		if queue.get_name() == channel_name:
			return channel_queues.index(queue)

def channel_queue_dequeue(queue_index):
    try:
        return channel_queues[queue_index].dequeue()
    except:
        logging.critical(f"Could not dequeue from {channel_queues[queue_index].get_name()}! In channel_queue_dequeue()")

def channel_queue_enqueue(filename, channel_name):
    if get_channel_queue_pos(channel_name) == None:
        logging.debug(f"channel queue created. ID: {channel_name}")
        channel_queues.append(Queue(channel_name))

    try:
        channel_queues[get_channel_queue_pos(channel_name)].enqueue(filename)
        logging.debug(f"{filename} added to channel queue {channel_name}")
    except:
        logging.critical("filename could not be added to channel queue! channel_queue_enqueue()")


bot.run(backgroundstuff.get_config('token'))