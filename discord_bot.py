from operator import is_
import backgroundstuff
import discord
from discord.ext import commands
import random
import logging
import asyncio
import time
import json
from my_queue import Queue

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.DEBUG)
language = backgroundstuff.load_json("config.json")["language"]
descriptions = backgroundstuff.load_json("Files/texts.json")["descriptions"][language]
chat_texts = backgroundstuff.load_json("Files/texts.json")["chat-texts"][language]
bot_description = descriptions["bot-description"]
status = backgroundstuff.load_json("Files/status.json")[language]
channel_queues = []

bot = commands.Bot(command_prefix='?', description=bot_description)
bot.remove_command('help')

bot.load_extension("cogs.chatcog")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logging.info("--- Bot ready ---")

# eventcontrolled functions
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    if member.voice is None: return
    if is_muted(member): return # uses member to get voice channel
    
    if before.channel is not after.channel and after.channel is not None:
        await asyncio.sleep(0.5)
        await voice_events("welcome", member)
        await bot.change_presence(activity=discord.Game(random.choice(status))) # changes discord status of bot
    elif after.self_deaf and not before.self_deaf:
        await voice_events("deaf", member)
    elif after.self_stream and not before.self_stream:
        await voice_events("stream", member)
    else: return

# starts eventcontrolled functions
async def voice_events(pEvent, member):
    username = str(member)[:-5]
    channel = member.voice.channel
    channel_name = channel.name
    logging.info(f"{pEvent} triggered for {username}")

    file = backgroundstuff.generate_text(usecase=pEvent, name=username)

    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)


'''
Commands
'''

# weather for given city (Still German!!!)
# TOKEN for weather API must be moved to config or somewhere else!!
@bot.command(brief=descriptions["weather"]["brief"], description=descriptions["weather"]["description"])
async def weather(ctx, city=""):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    if city == "":
        async with ctx.channel.typing():
            await ctx.send(chat_texts["weather"]["no-city"])
            return
        
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    
    async with ctx.channel.typing():
        file = backgroundstuff.weather_message(city)
        if file is None:
            await ctx.send(chat_texts["weather"]["no-weather"])
            return
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# random facts
@bot.command(brief=descriptions["fact"]["brief"],description=descriptions["fact"]["description"])
async def fact(ctx):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author

    file = backgroundstuff.generate_text("fact")
    if file is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["error"])
            return
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Sagt die Uhrzeit
@bot.command(brief=descriptions["timeOD"]["brief"], description=descriptions["timeOD"]["description"])
async def timeOD(ctx):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    file = backgroundstuff.get_time()
    if file is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["error"])
            return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)

# Beleidigt jemanden
@bot.command(brief=descriptions["insult"]["brief"], description=descriptions["insult"]["description"])
async def insult(ctx, name=""):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    if name == "":
        async with ctx.channel.typing():
            await ctx.send(chat_texts["insult"]["no-name"])
            return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    author = str(member)[:-5]
    file = backgroundstuff.generate_text("insult", target=name, author=author)
    if file is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["error"])
            return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)


@bot.command(brief=descriptions["joke"]["brief"], description=descriptions["joke"]["description"])
async def joke(ctx):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    file = backgroundstuff.generate_text("joke")
    if file is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["error"])
            logging.warning("Error in 'joke'. File is None")
            return

    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)


@bot.command(brief=descriptions["sendLove"]["brief"], description=descriptions["sendLove"]["description"])
async def sendLove(ctx, name):
    if is_muted(ctx.message.author):
        async with ctx.channel.typing():
            await ctx.send(chat_texts["muted"])
        return
    if ctx.message.author.voice is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["not-in-channel"])
            return
    if name == "":
        async with ctx.channel.typing():
            await ctx.send(chat_texts["sendLove"]["no-name"])
            return
    channel_name = ctx.message.author.voice.channel.name
    member = ctx.message.author
    origin = str(member)[:-5]
    file = backgroundstuff.generate_text("love", target=name, author=origin)
    if file is None:
        async with ctx.channel.typing():
            await ctx.send(chat_texts["error"])
            logging.warning("Error in 'sendLove'. File is None")
            return
    
    channel_queue_enqueue(file, channel_name)
    await queue_abspielen(member)


# Verbindet mit einem Channel, wenn es möglich ist
async def connect_when_possible(member):
    member_voice = member.voice.channel
    server = member.guild

    if not server.voice_client is None:
        return

    await member_voice.connect()
    logging.debug("Bot connected")


# Plays files from queue for channel of member
async def queue_abspielen(member):
    await connect_when_possible(member)

    server = member.guild
    voice_connection = server.voice_client # Needs existing connection to work!
    
    channel_name = member.voice.channel.name
    queue_index = get_channel_queue_pos(channel_name)

    while True:
        await connect_when_possible(member)
        datei = channel_queue_dequeue(queue_index) + ".mp3"
        logging.debug("f{datei} was deleted from queue")
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

def is_muted(member):
    events = backgroundstuff.load_json("Files/events.json")
    channel = member.voice.channel
    channel_id = channel.id
    
    if channel_id in events["bot-mute"]:
        mute_time = events["bot-mute"][channel_id]
        if int(time.time()) > mute_time:
            del events["bot-mute"][channel_id]
            with open ("Files/events.json", "w") as f:
                json.dump(events, f)
            return False
        else:
            return True

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


token = backgroundstuff.load_json("config.json")["token"]
if token == "":
    token = backgroundstuff.load_json("token.json")["token"]
bot.run(token)