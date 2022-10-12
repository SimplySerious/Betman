import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import random
from setup import contains_link, addlog


class Fun(commands.Cog):
    """Make the bot say whatever you want to or make it reply to a message you can edit later on. Yeah this is funnnnnn.
Oh and also, There's 8Ball."""
    def __init__(self, client):
        self.client = client

    @commands.command(name="Say", help='Repeats the Text.')
    async def Say(self, ctx, *, msg='You must add a text'):
        if contains_link(msg):
            await ctx.reply("nah fam, won't let you send links")
        else:
            addlog(f"{ctx.author.mention} Used Say: {msg}", self.client)
            await ctx.send(msg)

    @commands.command(name="Reply",
                      help='Repeats the Text while also replying.')
    async def Reply(self, ctx, *, msg='You must add a text'):
        if contains_link(msg):
            await ctx.reply("nah fam, won't let you send links", self.client)
        else:
            addlog(f"{ctx.author.mention} Used reply: {msg}", self.client)
            await ctx.reply(msg)

    @commands.command(
        name="8Ball",
        help='Ask a Question and get an answer. Can\'t be more simple.')
    async def _8Ball(self, ctx, *, question="I Can't Ask a Question, smh"):
        answers = ('As I see it, yes.', 'Ask again later.',
                   'Better not tell you now.', 'Cannot predict now.',
                   'Concentrate and ask again.', 'Don’t count on it.',
                   'It is certain.', 'It is decidedly so.', 'Most likely.',
                   'My reply is no.', 'My sources say no.',
                   'Outlook not so good.', 'Outlook good.',
                   'Reply hazy, try again.', 'Signs point to yes.',
                   'Very doubtful.', 'Without a doubt.', 'Yes.',
                   'Yes – definitely.', 'You may rely on it.')
        emb = discord.Embed(
            description=
            f"Question: {question}\nAnswer: {random.choice(answers)}",
            color=discord.Colour.blue())
        emb.set_footer(text=f"requested by {ctx.author.name}",
                       icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        if not contains_link(question):
            await ctx.send(embed=emb)
        else:
            await ctx.send("Nah fam, can't let you post links")
