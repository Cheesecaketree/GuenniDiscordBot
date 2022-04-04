import discord
from discord.ext import commands
import backgroundstuff
import json
import time

class ChatCog(commands.Cog):
    # Pure chaos because I have no idea how to do this properly.
    language = backgroundstuff.load_json("config.json")["language"]
    descriptions = {}
    chat_texts = {}
    descriptions = backgroundstuff.load_json("Files/texts.json")
    descriptions = descriptions["descriptions"][language]
    chat_texts = backgroundstuff.load_json("Files/texts.json")
    chat_texts = chat_texts["chat-texts"][language]
    def __init__(self,bot):
        self.bot = bot
        self.descriptions = self.descriptions
        self.chat_texts = self.chat_texts
        
    def get_description(self, key1, key2 = None, key3 = None):
        if key2 is not None:
            if key3 is not None:
                return self.descriptions[key1][key2][key3]
            else:
                return self.descriptions[key1][key2]
        return self.descriptions[key1]
    
    def get_chat_texts(self):
        return self.chat_texts
    
    @commands.command(hidden = True)
    async def ping(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(self.chat_texts["ping"].format(round(self.bot.latency, 1)))
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            color = discord.Color.orange() )
        embed.set_author(name="Help")
        embed.add_field(name="?fact", value=(self.get_description("fact","brief")), inline=False)
        embed.add_field(name="?time", value=(self.get_description("timeOD", "brief")), inline=False)
        embed.add_field(name="?joke", value=(self.get_description("joke", "brief")), inline=False)
        embed.add_field(name="?weather <city>", value=(self.get_description("weather", "brief")), inline=False)
        embed.add_field(name="?insult <name>", value=(self.get_description("insult", "brief")), inline=False)
        embed.add_field(name="?sendLove <name>", value=(self.get_description("sendLove", "brief")), inline=False)
        
        await ctx.send(embed=embed)
    
    # Admins can mute the bot for an amount of time.
    @commands.command(hidden=True, brief=descriptions["mute"]["brief"], description=descriptions["mute"]["description"])
    async def mute(self, ctx, minutes=None, channel=None):
        if channel is None or minutes is None:
            await ctx.send(self.chat_texts["mute"]["usage"])
        
        config = backgroundstuff.load_json("config.json")
        
        allowed_roles = config["privileged-roles"]
        author_roles = ctx.message.author.roles
        
        for role in author_roles:
            if role.name not in allowed_roles:
                await ctx.send(self.chat_texts["mute"]["role-error"])
                return
        
        max_mute = config["max-mute"]
        if minutes > max_mute:
            await ctx.send(self.chat_texts["mute"]["too-long"].format(max_mute))
            return
        
        channel = channel.lower()
        events = backgroundstuff.load_json("Files/events.json")
        
        if channel in events["bot-mute"]:
            current_mute = events["bot-mute"][channel]
            if current_mute > int(time.time() + int(minutes * 60)):
                await ctx.send(self.chat_texts["mute"]["already-muted"].format(int(current_mute - int(time.time())) / 60))
                return
            
        mute_time = int(time.time()) + (int(minutes) * 60)
        events["bot-mute"][channel] = mute_time
        with open("Files/events.json", "w") as f:
            json.dump(events, f)
        await ctx.send(self.chat_texts["mute"]["confirmation"].format(minutes))
    
    @commands.command(hidden=True, brief=descriptions["unmute"]["brief"], description=descriptions["unmute"]["description"])
    async def unmute(self, ctx, channel=None):
        if channel is None:
            await ctx.send(self.chat_texts["unmute"]["usage"])
        
        config = backgroundstuff.load_json("config.json")
        
        allowed_roles = config["privileged-roles"]
        author_roles = ctx.message.author.roles
        
        for role in author_roles:
            if role.name not in allowed_roles:
                await ctx.send(self.chat_texts["unmute"]["role-error"])
                return
        
        channel = channel.lower()
        events = backgroundstuff.load_json("Files/events.json")
        
        if channel in events["bot-mute"]:
            del events["bot-mute"][channel]
            with open("Files/events.json", "w") as f:
                json.dump(events, f)
            await ctx.send(self.chat_texts["unmute"]["confirmation"])
        else:
            await ctx.send(self.chat_texts["unmute"]["not-muted"])
    
    
    # Debug only.
    @commands.command(hidden=True)
    async def print_status(self, ctx):
        with open("Files/events.json", "r") as f:
            status = json.load(f)
            await ctx.send(status)
            
            
    # deletes messages.
    @commands.command(hidden=True, pass_context = True, brief=descriptions["clear"]["brief"], description=descriptions["clear"]["description"])
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        
    

def setup(bot):
    bot.add_cog(ChatCog(bot))