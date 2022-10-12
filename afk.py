import discord
from discord.ext import commands
from replit import db
from time import time
from setup import contains_link,dtime,addlog
from datetime import datetime
def afksave():#copies data from memory to storage
    db["afkdata"] = afkdict

class AFK(commands.Cog):
    def __init__(self, client):
        global afkdict
        self.client = client
        try:
            afkdict=db["afkdata"]
            en='\n'
            addlog(f"""AFK data loaded sucessfully
Existing AFK's({len(afkdict)}):
{''.join(f"{en}<@{userid}>: **{afkdict[userid][0]}**; `{dtime(int(time())-afkdict[str(userid)][1]+1)} ago`" for userid in afkdict)}""",client)
        except:
            afkdict={}
            db["afkdata"]=afkdict
            addlog("AFK data was empty, dumped an empty dictionary instead",client)
    @commands.Cog.listener()
    async def on_message(self,msg):
        if not msg.author.bot and len(msg.content)!=0 and msg.content[0]!='=' and msg.content[:7].lower()!='oho afk':

            for ping in msg.mentions:#alerting users that the pinged guy is afk
                if str(ping.id) in afkdict:
                    await msg.channel.send(f"{ping.mention} is AFK: {afkdict[str(ping.id)][0]}; `{dtime(int(time())-afkdict[str(ping.id)][1]+1)}` ago",delete_after=10)
            if str(msg.author.id) in afkdict:#removing an afk
                del afkdict[str(msg.author.id)]
                afksave()
                await msg.reply("Hey, you. You're finally awake. Anyways, i removed your AFK",delete_after=10)
                addlog(f"AFKs={len(afkdict)}; an AFK was removed by {msg.author.mention}",self.client)
                try:
                    if msg.author.display_name[:5]=="[AFK]" and msg.guild.me.guild_permissions.manage_nicknames:
                        if msg.author.nick[5:]==msg.author.name:
                            await msg.author.edit(nick=None)
                        else:
                            await msg.author.edit(nick=msg.author.nick[5:])
                except Exception as error:
                    addlog(error,self.client)

    @commands.command(name="AFK", help='Sets Your AFK. These AFKs apply to every Mutual Server')
    async def AFK(self,ctx,*, msg='AFK'):
        if len(msg)<=256:
            if contains_link(msg):
                await ctx.reply("nah fam, cant let you post links")
            else:
                await ctx.reply(f"I set your AFK: {msg}")
                if str(ctx.author.id) in afkdict:
                    afkdict[str(ctx.author.id)]=(msg,afkdict[str(ctx.author.id)][1])
                    addlog(f"AFKs={len(afkdict)}; an AFK was updated by {ctx.author.mention}: {msg}",self.client)
                else:
                    afkdict[str(ctx.author.id)]=(msg,int(time()))
                    addlog(f"AFKs={len(afkdict)}; an AFK was added by {ctx.author.mention}: {msg}",self.client)
                afksave()
                try:
                    if ctx.author.display_name[:5]!="[AFK]" and ctx.guild.me.guild_permissions.manage_nicknames:
                        await ctx.author.edit(nick=f"[AFK]{ctx.author.display_name}")
                except Exception as error:
                    addlog(error,self.client)
        else:
            await ctx.reply("Sorry, you message exceeds 256 characters. Maybe try to shorten out your feelings.")

    @commands.command(name="AFKRemove", help='Removes a Person\'s AFK manually.')
    @commands.has_role(725660115998343178)
    @commands.has_permissions(manage_messages=True)
    async def AFKRemove(self,ctx,*, user:discord.Member=None):
        if str(user.id) in afkdict:#removing an afk
            del afkdict[str(user.id)]
            afksave()
            try:
                if user.display_name[:5]=="[AFK]":#removing [AFK] from stuck nicknames if by chance the bot resets
                    if user.display_name[5:]==user.name:
                        await user.edit(nick=None)
                    else:
                        await user.edit(nick=user.display_name[5:])
            except:pass
            await ctx.reply(f"AFK removed from {user.mention} sucessfully")
            addlog(f"AFKs={len(afkdict)}; {user.mention}'s AFK was manually removed by {ctx.author.mention}",self.client)
        elif user==None:
            await ctx.reply("Please Specify a User")
        else:
            await ctx.reply("No such User exists in the Database")

    @commands.command(name="AFKs", help='Shows existing AFKs.')
    @commands.has_role(725660115998343178)
    async def AFKs(self,ctx):
        text=''.join(f"<@{userid}>: **{afkdict[userid][0]}**; `{dtime(int(time())-afkdict[str(userid)][1]+1)} ago`\n" for userid in afkdict)
        if text=='':
            text="None"
        emb=discord.Embed(title=f"All active AFKs ({len(afkdict)})",description=text,color=discord.Colour.blue())
        emb.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.utcnow()
        await ctx.reply(embed=emb)
