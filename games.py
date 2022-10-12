import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from setup import yes, no, end
from time import time
import random


class Games(commands.Cog):
    """Some Games you can play with Me or your Friends (Hopefully).
Most of the Games require Me having permissions to Embed Links soo play these Games where they are supposed to"""
    def __init__(self, client):
        self.client = client

    @commands.command(name="TicTacToe",
                      aliases=['TTC'],
                      help='A Multi-Player Game of TicTacToe.')
    async def TicTacToe(self, ctx, opponent: discord.Member = None):
        time = datetime.utcnow()

        #twitter dont cancel me pls these functions were all named accidentally
        def chka(msg):  #checksauthor
            return msg.author == ctx.author

        def chko(msg):  #checksopponenet
            return msg.author == opponent

        def chkw(data):  #checks if someone won
            w = False
            checks = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                      (2, 5, 8), (0, 4, 8), (2, 4, 6))
            for check in checks:
                if data[check[0]] == data[check[1]] == data[check[2]] and data[
                        check[0]] != None:
                    w = True
            return w

        def transv(msg):  #translates value
            if len(msg) == 1 and msg[0] in (str(n) for n in range(1, 10)):
                return int(msg[0]) - 1
            elif len(msg) == 2 and msg[0].lower() in (
                    'a', 'b', 'c') and msg[1] in ('1', '2', '3'):
                ans = -1
                if msg[0].lower() == 'b':
                    ans += 3
                if msg[0].lower() == 'c':
                    ans += 6
                return ans + int(msg[1])
            else:
                return None

        def transd(data):  #visualises data
            txt = ''
            for n in range(9):
                if n % 3 == 0:
                    txt += '\n'
                if data[n] == None:
                    txt += '‎⚫'
                elif data[n] == True:
                    txt += '⭕'
                elif data[n] == False:
                    txt += '❌'
            return txt

        def aoro(
            auth
        ):  #simple function which returns either author or opponent based on auth value
            if auth == True:
                return ctx.author.mention
            else:
                return opponent.mention

        if opponent == None:
            await ctx.send("You must specify a User")
        elif opponent == self.client.user:
            await ctx.send("I refuse to play")
        elif opponent == ctx.author:
            await ctx.send(
                "You played yourself. Wait, you can't. (definitely not a stolen joke)"
            )
        else:
            emb = discord.Embed(
                description=
f"""use `a`,`b` or `c` for the rows and `1`,`2` or `3` for the columns, just like in chess (for example: `b2` for middle slot).
or use numbers between `1` to `9` accordingly.
    {opponent.mention}, Do You wanna play too? (`yes/no`)""",
                color=discord.Colour.blue())
            emb.set_author(name=opponent.name, icon_url=opponent.avatar_url)
            emb.set_footer(text=f"Requested by {ctx.author.name}",
                           icon_url=ctx.author.avatar_url)
            emb.timestamp = time
            await ctx.send(embed=emb)
            try:
                msg = await self.client.wait_for('message',
                                                 check=chko,
                                                 timeout=30)
                if msg.content.lower() in yes:
                    dat = []
                    for n in range(9):
                        dat.append(None)
                    auth = True
                    while None in dat and not chkw(dat):
                        try:
                            if auth:
                                emb = discord.Embed(
                                    description=f"Its your turn.{transd(dat)}",
                                    color=discord.Colour.gold())
                                emb.set_author(name=f"{ctx.author.name},",
                                               icon_url=ctx.author.avatar_url)
                                emb.timestamp = time
                                await msg.reply(embed=emb)
                                msg = await self.client.wait_for('message',
                                                                 check=chka,
                                                                 timeout=30)
                            else:
                                emb = discord.Embed(
                                    description=f"Its your turn.{transd(dat)}",
                                    color=discord.Colour.dark_gold())
                                emb.set_author(name=f"{opponent.name},",
                                               icon_url=opponent.avatar_url)
                                emb.timestamp = time
                                await msg.reply(embed=emb)
                                msg = await self.client.wait_for('message',
                                                                 check=chko,
                                                                 timeout=30)
                            if transv(msg.content) != None:
                                if dat[transv(msg.content)] == None:
                                    dat[transv(msg.content)] = auth
                                    auth = not auth
                                else:
                                    await msg.reply(
                                        "That place is taken. Try a different one"
                                    )
                            elif msg.content in end:
                                await msg.reply(
                                    "Understandable, have a great day")
                                return
                            else:
                                await msg.reply("Invalid Value, Try Again")
                        except asyncio.TimeoutError:
                            await ctx.send(
                                f"{aoro(auth)} Waited too long, Cancelling the game"
                            )
                            return
                    if chkw(dat):
                        emb = discord.Embed(
                            description=
                            f"{aoro(not auth)} wins the match. GG{transd(dat)}",
                            color=discord.Colour.green())
                        emb.set_author(name=f"{ctx.author.name}",
                                       icon_url=ctx.author.avatar_url)
                        emb.timestamp = time
                        await msg.reply(embed=emb)
                    else:
                        emb = discord.Embed(
                            description=f"Its a Draw{transd(dat)}",
                            color=discord.Colour.red())
                        emb.set_author(name=f"{ctx.author.name}",
                                       icon_url=ctx.author.avatar_url)
                        emb.timestamp = time
                        await msg.reply(embed=emb)
                elif msg.content.lower() in no:
                    await msg.reply("Understandable, have a great day")
                else:
                    await msg.reply("I will take that as a no")
            except asyncio.TimeoutError:
                await ctx.send(
                    f"{opponent.mention} Waited too long, Cancelling the game")

    @commands.command(
        name='RockPaperScissors',
        aliases=('StonePaperScissors', 'RPS', 'SPS'),
        help='A Single-Player/Multi-Player Game of Rock Paper Scissors.')
    async def RockPaperScissors(self, ctx, opponent: discord.Member = None):
        s = ('`Rock`', '`Paper`', '`Scissors`')
        s2 = (('stone', 'rock', 'st', 'r'), ('paper', 'pa', 'p'), ('scissors',
                                                                   'sc', 's'))

        def chka(msg):
            return msg.author == ctx.author

        def chko(msg):
            return msg.author == opponent

        def aoinv(mem):  #author or opponent inverse
            if mem == ctx.author.mention:
                return opponent.mention
            elif mem == opponent.mention:
                return ctx.author.mention
            else:
                raise ValueError

        if opponent == ctx.author:
            await ctx.send("You played yourself. Wait, you can't. (definitely not a stolen joke)")
        elif opponent == None:
            await ctx.send("You must specify a User")
        elif opponent == self.client.user:
            await ctx.send("Tell me your choice between `rock` , `paper` or `scissors`, I wont cheat.")
            try:
                msg = await self.client.wait_for('message',
                                                 check=chka,
                                                 timeout=30)
                u = None  #user's answer integer
                for n in range(3):
                    if msg.content.lower() in s2[n]:
                        u = n
                if u != None:
                    m = random.randint(0, 2)
                    if u == (m + 1) % 3:
                        winner = "You win"
                    elif (u + 1) % 3 == m:
                        winner = "I win"
                    else:
                        winner = "Nobody wins"
                    await msg.reply(
                        f"You choose {s[u]}, I chose {s[m]}, **{winner}!!**"
                    )
                else:
                    await msg.reply("Sorry i wasnt able to understand that.")
            except asyncio.TimeoutError:
                await ctx.send("You Waited too long, Cancelling the game")
        else:
            await ctx.send(f"""I will count from 3 backwards.
both players have to type `rock`, `paper` or `scissors` the moment I stop counting.
{opponent.mention}, Do you wanna play too? (`yes/no`)""")
            try:
                msg = await self.client.wait_for('message',
                                                 check=chko,
                                                 timeout=30)
                if msg.content.lower() in yes:
                    msg = await ctx.send(content="Message your choice in 3,")
                    await asyncio.sleep(1)
                    await msg.edit(content="Message your choice in 3,2,")
                    await asyncio.sleep(1)
                    await msg.edit(content="Message your choice in 3,2,1,")
                    await asyncio.sleep(1)
                    await msg.edit(
                        content="Message your choice in 3,2,1,**NOW!!**")
                    tlist = []

                    def chk2(msg):
                        nonlocal tlist
                        fail = True
                        if msg.author in (ctx.author, opponent):
                            for n in range(3):
                                if msg.content.lower() in s2[n]:
                                    if len(
                                            tlist
                                    ) == 1 and msg.author.mention == tlist[0][
                                            0]:
                                        return False
                                    tlist.append([msg.author.mention,n,time()])
                                    self.client.loop.create_task(
                                        msg.add_reaction('\N{THUMBS UP SIGN}'))
                                    fail = False
                            if fail:
                                self.client.loop.create_task(
                                    msg.add_reaction('\N{CROSS MARK}'))
                        return len(tlist) == 2

                    try:
                        msg = await self.client.wait_for('message',
                                                         check=chk2,
                                                         timeout=3)
                        if tlist[0][1] == tlist[1][1]:
                            await ctx.send(
f"""Both of the players chose {s[tlist[0][1]]}
**Its a draw** with {tlist[0][0]} answering `{int((tlist[1][2]-tlist[0][2])*1000)} ms` early"""
                            )
                        elif tlist[0][1] == (tlist[1][1] + 1) % 3:
                            await ctx.send(
f"""{tlist[0][0]} chose {s[tlist[0][1]]}, {tlist[1][0]} chose {s[tlist[1][1]]}
{tlist[0][0]} won while answering `{int((tlist[1][2]-tlist[0][2])*1000)} ms` early"""
                            )
                        elif (tlist[0][1] + 1) % 3 == tlist[1][1]:
                            await ctx.send(
f"""{tlist[0][0]} chose {s[tlist[0][1]]}, {tlist[1][0]} chose {s[tlist[1][1]]}
{tlist[1][0]} won tho {tlist[0][0]} answered `{int((tlist[1][2]-tlist[0][2])*1000)} ms` early
There is a chance {tlist[1][0]} cheated""")
                        else:
                            await ctx.send("some error eccored")
                    except asyncio.TimeoutError:
                        if len(tlist) == 1:
                            await ctx.send(
                                f"{aoinv(tlist[0][0])} took too long to respond correctly, Cancelling the game"
                            )
                        else:
                            await ctx.send(
                                f"both {ctx.author.mention} and {opponent.mention} took too long to respond correctly, Cancelling the game"
                            )
                elif msg.content.lower() in no:
                    await ctx.send("Understandable, have a great day")
                else:
                    await ctx.send("I will take that as a no")
            except asyncio.TimeoutError:
                await ctx.send(
                    f"{opponent.mention} Waited too long to respond, Cancelling the game"
                )

    @commands.command(
        name="Guess",
        help='A Single-Player Game where I try to guess your Number.')
    async def Guess(self, ctx, limit=99):
        def chka(msg):
            return msg.author == ctx.author

        while True:
            time = datetime.utcnow()
            emb = discord.Embed(description=f"""
Welcome to guess the number.
In this game, The goal is that I should be able to guess whatever number you had in your mind by the end of the game.

Rules of this game:
> 1. Your number must be a natural number lower than {limit}. 
> 2. I will send a set amount of groups of numbers one-by-one and ask you if your number is in the current group. reply yes or no accordingly.
> 3. You can end this game anytime by saying "end".

Do you want to start the game? (yes/no)""",
                                color=discord.Colour.blue())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            emb.timestamp = time
            await ctx.send(embed=emb)

            try:
                msg = await self.client.wait_for('message',
                                                 check=chka,
                                                 timeout=30)
                if msg.content.lower() in yes:
                    x = 1
                    ans = 0
                    while x < (limit + 1):
                        nos = ''
                        write = False
                        for n in range(x, limit + 1):
                            if n % x == 0:
                                write = not write
                            if write == True:
                                nos += str(
                                    f"{'0' * (len(str(limit)) - len(str(n)))}{n}, "
                                )
                        nos = nos[:-2] + '.'
                        try:
                            emb = discord.Embed(color=discord.Colour.blue())
                            emb.set_author(name=ctx.author,
                                           icon_url=ctx.author.avatar_url)
                            emb.add_field(
                                name=
                                "Is Your No Present Between The Following Group of Numbers?",
                                value=f"```{nos}```")
                            emb.timestamp = time
                            await msg.reply(embed=emb)
                            ask = await self.client.wait_for('message',
                                                             check=chka,
                                                             timeout=60)
                            if ask.content.lower() in yes:
                                ans += x
                            elif ask.content.lower() in no:
                                pass
                            elif ask.content.lower() in end:
                                emb = discord.Embed(
                                    description="Ok, Cancelling the game",
                                    color=discord.Colour.red())
                                emb.set_author(name=ctx.author,
                                               icon_url=ctx.author.avatar_url)
                                emb.timestamp = time
                                await msg.reply(embed=emb)
                                return
                            else:
                                emb = discord.Embed(
                                    description=
                                    "Invalid Option, use some variant of yes or no\nif you dont wanna play, reply end or wait 60 seconds",
                                    color=discord.Colour.red())
                                emb.set_author(name=ctx.author,
                                               icon_url=ctx.author.avatar_url)
                                emb.timestamp = time
                                await msg.reply(embed=emb)
                                continue
                        except asyncio.TimeoutError:
                            emb = discord.Embed(
                                description=
                                "You waited too long, Cancelling the game",
                                color=discord.Colour.red())
                            emb.set_author(name=ctx.author,
                                           icon_url=ctx.author.avatar_url)
                            emb.timestamp = time
                            await ctx.send(embed=emb)
                            return
                        x *= 2
                    if ans == 0 or ans > limit:
                        emb = discord.Embed(
                            description=
                            "Why did you just spam, read carefully next time.",
                            color=discord.Colour.red())
                        emb.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar_url)
                        emb.timestamp = time
                        await msg.reply(embed=emb)

                    else:
                        emb = discord.Embed(
                            description=f"**Your number is {ans}**",
                            color=discord.Colour.blue())
                        emb.set_author(name=ctx.author,
                                       icon_url=ctx.author.avatar_url)
                        emb.timestamp = time
                        await msg.reply(embed=emb)

                elif msg.content.lower() in no:
                    emb = discord.Embed(description="Ok, Cancelling the game",
                                        color=discord.Colour.red())
                    emb.set_author(name=ctx.author,
                                   icon_url=ctx.author.avatar_url)
                    emb.timestamp = time
                    await msg.reply(embed=emb)
                    return
                else:
                    emb = discord.Embed(
                        description=
                        "Invalid Option, use some variant of yes or no",
                        color=discord.Colour.blue())
                    emb.set_author(name=ctx.author,
                                   icon_url=ctx.author.avatar_url)
                    emb.timestamp = time
                    await msg.reply(embed=emb)
                    return
            except asyncio.TimeoutError:
                emb = discord.Embed(
                    description="You waited too long, Cancelling the game",
                    color=discord.Colour.blue())
                emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                emb.timestamp = time
                await ctx.send(embed=emb)
                return
            return
