import random
import discord
from discord.ext import commands
import backgroundstuff
import logging
import asyncio

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.INFO)
channel_queues = []

class audio_management(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Verbindet mit einem Channel, wenn es möglich ist
    async def connect_when_possible(self, member):
        member_voice = member.voice.channel
        server = member.guild

        if not server.voice_client is None:
            return

        await member_voice.connect()
        logging.debug("Bot connected")


    # Spielt files aus der Queue ab
    async def queue_abspielen(self, member):
        await self.connect_when_possible(self, member)
        server = member.guild
        voice_connection = server.voice_client
        channel_name = member.voice.channel.name
        queue_index = self.get_channel_queue_pos(self, channel_name)

        while True:
            await self.connect_when_possible(self, member)
            datei = self.channel_queue_dequeue(self, queue_index)
            logging.debug("f{datei} wurde aus queue gelöscht")
            voice_connection.play(discord.FFmpegPCMAudio(str(datei)))
            logging.info(f"{datei} is being played.")
            while voice_connection.is_playing():
                pass
            channel_queues[queue_index].done()
            backgroundstuff.delete_file(datei)

            if channel_queues[queue_index].isEmpty():
                await voice_connection.disconnect()
                voice_connection.cleanup()
                logging.debug("Queue is empty. Bot has disconnected.")
                return
            else:
                await voice_connection.disconnect()
                voice_connection.cleanup()
                logging.debug("Queue not empty. Bot is playing next file")


    class Queue:
        def __init__(self, name):
            self.queue = asyncio.Queue()
            self.id = name
            
        def isEmpty(self):
            return self.queue.empty()
        
        def enqueue(self, item):
            self.queue.put_nowait(item)
            
        def done(self):
            self.queue.task_done()

        def dequeue(self):
            if not self.queue.empty():
                return self.queue.get_nowait()
            
        def get_name(self):
            return self.id

    def get_channel_queue_pos(self, channel_name):
        for queue in channel_queues:
            if queue.get_name() == channel_name:
                return channel_queues.index(queue)

    def channel_queue_dequeue(self, queue_index):
        try:
            return channel_queues[queue_index].dequeue()
        except:
            logging.critical(f"Could not dequeue from {channel_queues[queue_index].get_name()}! In channel_queue_dequeue()")

    def channel_queue_enqueue(self, filename, channel_name):
        if self.get_channel_queue_pos(channel_name) == None:
            logging.debug(f"channel queue created. ID: {channel_name}")
            channel_queues.append(self.Queue(channel_name))

        try:
            channel_queues[self.get_channel_queue_pos(channel_name)].enqueue(filename)
            logging.debug(f"{filename} added to channel queue {channel_name}")
        except:
            logging.critical("filename could not be added to channel queue! channel_queue_enqueue()")


def setup(client):
    client.add_cog(audio_management(client))