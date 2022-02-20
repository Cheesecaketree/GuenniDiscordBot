import discord
from discord.ext import commands

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
        
def setup(bot):
    bot.add_cog(ChatCog(bot))