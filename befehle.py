'''
!!!WIRD NICHT GENUTZT!!!
'''




import random
import discord
from discord.ext import commands
import backgroundstuff


class befehle(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Sagt das Wetter für den angegebenen Ort
    @commands.command(brief="Aktuelles Wetter", description="Günni kommt in deinen Voicechannel und sagt das Wetter für den angegebenen Ort.\n Verwendung: ?wetter *STADT*")
    async def wetter(self, ctx, *args):
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        print(str(ctx.message.author) + " möchte das Wetter wissen")

        stadt = ' '.join(args)  # Fügt den Teil nach dem Befehl zu einem String zusammen
        wetter = backgroundstuff.get_weather(stadt)  # holt sich das Wetter
        if wetter == None:
            print("Fehler beim Wetter! Verbindung wird getrennt")
            await ctx.send("Diese Stadt scheint es nicht zu geben... ")
            await ctx.send("Achte darauf, dass du die Stadt richtig geschrieben hast!")
            return
        backgroundstuff.generate_voice(wetter,"wetter")

        # Verbindet sich mit dem Voicechannel und spielt die Nachricht ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "wetter.mp3")

        backgroundstuff.delete_file("wetter.mp3")
        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))

    # Sagt einen zufälligen Fakt
    @commands.command(brief='Sagt einen Fakt',description='Günni kommt in deinen Channel und sagt einen zufälligen Fakt.\n Nichts weiter zu beachten :)')
    async def fakt(self, ctx):
        await ctx.message.delete()
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        print(str(ctx.message.author) + " möchte einen Fakt bekommen")

        fakt = backgroundstuff.get_useless_fact()  # holt sich den Fakt
        if not fakt == None:
            backgroundstuff.generate_voice("Wusstest du schon: " + fakt,"fakt")
            await ctx.send(fakt)
        else:
            await ctx.send("Es gab einen Fehler! Bitte später erneut versuchen")

        # Spielt die Audiodatei im Channel ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "fakt.mp3")

        backgroundstuff.delete_file("fakt.mp3")
        
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))

    # Sagt die Uhrzeit
    @commands.command(brief='Uhrzeit', description="Sagt die aktuelle Uhrzeit.")
    async def uhrzeit(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        print(str(ctx.message.author) + " möchte die Uhrzeit wissen")

        backgroundstuff.generate_voice(backgroundstuff.get_uhrzeit(), "uhrzeit")

        # Verbindung mit Channel herstellen und Audio abspielen
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "uhrzeit.mp3")

        backgroundstuff.delete_file("uhrzeit.mp3")

        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))
        print("Uhrzeit erfolgreich gesagt")
        print("")

    # Beleidigt jemanden
    @commands.command(brief='Kann Leute beleidigen.', description="Kommt zu dir und beleidigt die angegebene Person.\n Verwendung: ?beleidige *Name*")
    async def beleidige(self, ctx, *args):
        opfer = ' '.join(args)
        author = str(ctx.message.author)[:-5]
        
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        if backgroundstuff.name_boese(opfer):
            print("{} wollte einen bösen Namen verwenden!".format(author))
            await ctx.send("Abgelehnt")
            return

        print("{author} möchte {opfer} beledigen".format(author=author, opfer=opfer))
        nachricht = backgroundstuff.get_beleidigung_liebe(opfer, author, False)
        backgroundstuff.generate_voice(nachricht, "beleidigung")

        # Spielt die Audiodatei im Channel ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "beleidigung.mp3")

        backgroundstuff.delete_file("beleidigung.mp3")
        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))
        print("")

    # Sagt was nettes
    @commands.command(brief='Kann Leute mögen.', description="Kommt zu dir und sagt, dass du die angegebene Person magst. \n Voll auf liebe und so :) \n Verwendung: ?sendeLiebe *Name*")
    async def sendeLiebe(self, ctx, *args):
        ziel = ' '.join(args)
        author = str(ctx.message.author)[:-5]
        
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        if backgroundstuff.name_boese(ziel):
            print("{} wollte einen bösen Namen verwenden!".format(author))
            await ctx.send("Abgelehnt")
            return

        print("{author} möchte {opfer} Liebe senden".format(author=author, opfer=ziel))
        nachricht = backgroundstuff.get_beleidigung_liebe(ziel, author, True)
        backgroundstuff.generate_voice(nachricht, "liebe")

        # Spielt die Audiodatei im Channel ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "liebe.mp3")

        backgroundstuff.delete_file("liebe.mp3")
        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))
        print("")

    # Sagt was nettes oder beleidigt
    @commands.command(brief='Kann Leute mögen oder beleidigen.', description="Kommt zu dir und mag oder beleidigt die angegebene Person. \n Lustig! \n Verwendung: ?machwasmit *Name*")
    async def machwasmit(self, ctx, *args):
        ziel = ' '.join(args)
        author = str(ctx.message.author)[:-5]
        
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return
        if backgroundstuff.name_boese(ziel):
            print("{} wollte einen bösen Namen verwenden!".format(author))
            await ctx.send("Abgelehnt")
            return

        print("{author} möchte {opfer} erwähnen senden".format(author=author, opfer=ziel))
        nachricht = backgroundstuff.get_beleidigung_liebe(ziel, author, bool(random.getrandbits(1)))
        backgroundstuff.generate_voice(nachricht, "machwas")

        # Spielt die Audiodatei im Channel ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "machwas.mp3")

        backgroundstuff.delete_file("machwas.mp3")
        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht".format(ctx.message.author))
        print("")

    # Löscht Nachrichten in einem Channel
    @commands.command(pass_context = True, brief="Löscht Nachrichten im Channel", description="Löscht standardmäßig 5 Nachrichten, mehr, wenn mehr angegeben wird.")
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    # Spielt einen Teil von einem Kraftwerksong
    @commands.command(brief='Die Roboter.', description="...")
    async def roboter(self, ctx, *args):
        if ctx.message.author.voice is None:
            await ctx.send("Für diesen Befehl musst du in einem voice channel sein")
            return

        # Spielt die Audiodatei im Channel ab.
        channel = ctx.message.author.voice.channel
        server = ctx.message.guild
        await verbinden_abspielen_gehen(channel, server, "Files/roboter.mp3")

        await ctx.message.delete()
        print("Nachricht von {} wurde gelöscht \n".format(ctx.message.author))


async def verbinden_abspielen_gehen(channel, server, datei:str):
    await channel.connect()
    voice_channel = server.voice_client

    print("datei wird abgespielt")
    voice_channel.play(discord.FFmpegPCMAudio(datei))

    while voice_channel.is_playing():
        pass
    if voice_channel.is_connected():
        print("Verbindung wird getrennt")
        await voice_channel.disconnect()
        print("{datei} wurde erfolgreich abgespielt!".format(datei=datei))
    else:
        print("Konnte Verbindung nicht trennen. Irgendwas scheint hier nicht richtig zu sein...")


def setup(client):
    client.add_cog(befehle(client))