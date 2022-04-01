from os import stat
import discord
from discord.ext import commands
import backgroundstuff
import json

class ChatCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(hidden = True)
    async def ping(self, ctx):
        await ctx.send('Pong! Ping beträgt: {0}ms'.format(round(self.bot.latency, 1)))
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            color = discord.Color.orange() )
        embed.set_author(name="Help")
        embed.add_field(name="?fakt", value="Sagt einen Fakt.", inline=False)
        embed.add_field(name="?uhrzeit", value="Sagt die Uhrzeit", inline=False)
        embed.add_field(name="?witz", value="Erzählt einen Witz", inline=False)
        embed.add_field(name="?wetter *Stadt*", value="Sagt das Wetter für den angegebenen Ort.", inline=False)
        embed.add_field(name="?beleidge *Name*", value="Beleidigt die angegebene Person", inline=False)
        embed.add_field(name="?sendeLiebe *Name*", value="Sendet Liebe an die angegebene Person", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(hidden=False, brief="Admin only", description="Sperrt den Bot für den angegebenen Zeitraum")
    async def mute(self, ctx, time, channel):
        allowed_roles = ["@admin", "@günnimensch", "@everyone"]
        await ctx.send("Der Bot wird für {} Minuten stummgeschaltet.".format(time))
        author = ctx.message.author
        roles = author.roles
        print(roles)
        for role in roles:
            print(role.name)
            if role.name in allowed_roles:
                print("accepted")
                status = backgroundstuff.get_status()
                status["bot-mute"][channel] = str(time)
            
                with open("Files/status.json", "w") as f:
                    json.dump(status, f)
            else:
                print("not accepted")
                
    @commands.command()
    async def print_status(self, ctx):
        with open("Files/status.json", "r") as f:
            status = json.load(f)
            await ctx.send(status)
            
                
                
    
    
def setup(bot):
    bot.add_cog(ChatCog(bot))