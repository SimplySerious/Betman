import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from time import time
from setup import dtime

runtm = time()


class Info(commands.Cog):
    """From Me to Others, I got everyone's Info covered"""
    def __init__(self, client):
        self.client = client

    @commands.command(name="Uptime",
                      aliases=['RunTime'],
                      help='Shows how long the Bot is running for.')
    async def UpTime(self, ctx):
        await ctx.send(
            f"I am up and running since `{dtime(int(time()-runtm))}`(`{datetime.utcfromtimestamp(runtm).strftime('%Y-%m-%d %H:%M:%S')} UTC`)."
        )

    @commands.command(name="Ping", help='Returns My Ping.')
    async def Ping(self, ctx):
        await ctx.send(f'Pog! `{round(self.client.latency * 1000)}ms`')

    @commands.command(name="Servers", help="Shows every server I'm in.")
    @commands.is_owner()
    async def Servers(self, ctx):
        emb = discord.Embed(color=discord.Colour.blue())
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        for guild in self.client.guilds:
            emb.add_field(name=guild.name, value=guild.id)
        await ctx.author.send(embed=emb)

    @commands.command(name="Invite", help='Returns My Invite Links.')
    async def Invite(self, ctx):
        emb = discord.Embed(title="Invite Links")
        emb.add_field(
            name="Invite me",
            value=
            "[here](https://discord.com/api/oauth2/authorize?client_id=817740081972510740&permissions=134564864&scope=bot)"
        )
        emb.add_field(name="Dev Server",
                      value="[here](https://discord.gg/z6UbT8w9Ym)")
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        await ctx.reply(embed=emb)

    @commands.command(name="Avatar",
                      aliases=['av', 'PFP'],
                      help="Shows User's Avatar.")
    async def Avatar(self, ctx, user: discord.Member = None):
        if user == None: user = ctx.author
        emb = discord.Embed(
            color=ctx.author.color,
            title=
            "oww I definately don't know whose pfp this link is for :point_down: ",
            description=f"[click me uwu]({user.avatar_url})")
        emb.set_author(name=f"{user.name}'s avatar", icon_url=user.avatar_url)
        emb.set_image(url=user.avatar_url)
        emb.set_footer(text=f"Requested by {ctx.author}",
                       icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        await ctx.send(embed=emb)

    @commands.command(name="User",
                      aliases=['UserInfo'],
                      help="Shows User's Info.")
    async def User(self, ctx, user: discord.Member = None):
        if user == None: user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        emb = discord.Embed(color=ctx.author.color, description=user.mention)
        emb.set_author(name=f"{user.name}'s info", icon_url=user.avatar_url)
        emb.set_thumbnail(url=user.avatar_url)
        emb.add_field(name="Created At",
                      value=user.created_at.strftime(date_format),
                      inline=True)
        if not isinstance(ctx.channel, discord.DMChannel) and user.roles != 1:
            emb.add_field(name="Joined At",
                          value=user.joined_at.strftime(date_format),
                          inline=True)
            text = ' '.join([r.mention for r in user.roles][:0:-1])
            if text == '':
                text = "None"
            if len(text) > 1024:
                text = f"Value beyond character limit ({len(text)}/1024)"
            emb.add_field(name=f"Roles [{len(user.roles)-1}]",
                          value=text,
                          inline=False)
        if not isinstance(ctx.channel, discord.DMChannel):
            text = ', '.join([
                p[0].replace('_', ' ').title() for p in user.guild_permissions
                if p[1]
            ])
            if text == '':
                text = "None"
            emb.add_field(name="Permissions", value=text)
        emb.set_footer(text=f"Requested by {ctx.author}",
                       icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        await ctx.send(embed=emb)

    @commands.command(name="PatchNotes",
                      help='Sends Developer Notes. Warning!! Longgggg.')
    async def PatchNotes(self, ctx):
        emb = discord.Embed(color=discord.Colour.blue(),
                            description=f"""
Patch Notes for {self.client.user.name}, My second bot
Contains every change. Only continue if you are Super Bored```
v1.0.0 (7/3/21) : Added Basic DadJokes.
v1.0.1 (7/3/21) : Added Ping Command.
v1.0.2 (7/3/21) : Added Variations of Dadjokes.
v1.0.3 (7/3/21) : Added 8Ball Command.
v1.0.4 (7/3/21) : Added Say Command.
v1.0.5 (7/3/21) : DadJokes will UNO Reverse When Misused.
v1.0.6 (7/3/21) : Added Custom Status.
v1.0.7 (7/3/21) : Added Herobrine.
v1.1.0 (8/3/21) : Added AFK Command.
v1.1.1 (8/3/21) : AFKs are now stored in the Internal Storage.
v1.1.2 (8/3/21) : Added AFKs command to check existing AFKs.
v1.1.3 (8/3/21) : Added @everyone, @here, and link filter.
v1.1.4 (8/3/21) : Added a 256 Character limit to AFK's reason.
v1.2.0 (8/3/21) : Added Error Handlers (Basically, now YOU get the error instead of me in the py shell).
v1.2.1 (9/3/21) : Some Commands now require specific Roles or Permissions, Thanks to v1.2.0.
v1.2.2 (9/3/21) : Added more Responses and made them less resource intensive.
v1.2.3 (9/3/21) : Added Patch Notes lol.
v1.2.4 (9/3/21) : Added Welcome Messages (later removed).
v1.2.5 (10/3/21): Added "Reply" command similar to "Say" command.
v1.2.6 (6/4/21) : AFK now changes User's NickName.
v1.2.7 (9/4/21) : People can now see how long you have been AFK for.
v1.2.8 (10/4/21): Bot won't remove your AFK if Your Message starts with '='.
v1.3.0 (5/5/21) : Added "Guess" Command which is basically a number guessing game(first game ever, pog).
v1.3.1 (5/5/21) : Added Userinfo Command.
v1.3.2 (14/5/21): Added RockPaperScissors Command (Single/MultiPlayer Game).
v1.3.3 (15/5/21): Added TicTacToe Command (MultiPlayer Game).
v1.3.4 (15/5/21): Added UpTime Command.
v1.3.5 (20/5/21): Made some Major changes and Bug fixes.
v1.3.6 (24/6/21): AFK command will now use previous AFK's Time if the User was already AFK and Made AFK Data more stable.
  ```""")
        emb.set_footer(text=f"Requested by {ctx.author}",
                       icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        await ctx.send(embed=emb)

    #things to add: blacklisted words, server properties(settings by admins)
