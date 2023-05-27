import sys
import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime
from time import time, strftime
from readabledelta import readabledelta
from games import Games
from afk import AFK
from dadjokes import DadJokes
from fun import Fun
from info import Info
from admin import Admin
from setup import yes, no, contains_link, addlog
import os
import webserver
import requests
from webserver import keep_alive

intent = discord.Intents(guilds=True, members=True, messages=True)
help_command = commands.DefaultHelpCommand(no_category='Help')
client = commands.Bot(command_prefix=('B ', 'b '),
                      case_insensitive=True,
                      intents=intent,
                      allowed_mentions=discord.AllowedMentions(
                          everyone=False,
                          users=False,
                          roles=False,
                          replied_user=True),
                      help_command=help_command)

client.add_cog(Games(client))
client.add_cog(DadJokes(client))
client.add_cog(Fun(client))
client.add_cog(Info(client))
client.add_cog(Admin(client))

@client.event
async def on_ready():
	client.logc = client.get_channel(847042152050851860)
	en = '\n'

	req = requests.get("https://discord.com/api/path/to/the/endpoint")
	addlog(
	    f'JSON:{en}{"".join([f"{n}: `{req.headers[n]}`{en}" for n in req.headers])}',
	    client)
	await client.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.listening, name="Inner Voices"))
	en = '\n'
	addlog(
	    f"""{client.user} has connected to Discord!
    Joined Guilds ({len(client.guilds)}):
    {''.join(f"{en}{guild.name}" for guild in client.guilds)}""", client)
	client.add_cog(AFK(client))


@client.event
async def on_guild_join(guild):
	addlog(f"I was added to {guild.name}", client)
	emb = discord.Embed(
	    title="Umm Hi",
	    description=
	    "Thanks for adding me into your server sensai.\nSeems like you are a beta tester",
	    color=discord.Colour.blue())
	for chan in guild.text_channels:
		channel = client.get_channel(chan.id)
		try:
			await channel.send(embed=emb)
			break
		except:
			pass


@client.event
async def on_command_error(ctx, error):
	addlog(error, client)
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(":no_entry_sign: You lack permissions to do so.")
	elif isinstance(error, commands.CommandInvokeError):
		await ctx.send(
		    f""":no_entry_sign: An Error occured inside the command. That's Usually Because I lack permission to embed links here.
Ping:`{round(client.latency * 1000)}ms`
Error Info: `{error}`""")
		raise error
	elif isinstance(error, commands.CommandNotFound):
		await ctx.reply(':no_entry_sign: Command not found.')
	elif isinstance(error,
	                commands.MissingRole):  #lacks level 10 (command afks)
		await ctx.reply(f':no_entry_sign: {error}.')
	elif isinstance(error, commands.MissingAnyRole
	                ):  #lacks moderator and level 10 (command say, 8ball)
		await ctx.reply(f':no_entry_sign: {error}.')
	elif isinstance(error, commands.MissingPermissions):
		await ctx.reply(":no_entry_sign: You lack permission to do so.")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.reply(":no_entry_sign: Member Not Found")
	elif isinstance(error, commands.BadArgument):
		await ctx.reply(f":no_entry_sign: Bad Parameter Invoked")
	else:
		raise error


keep_alive()
token = os.environ['betmantoken']
client.run(token)
#top kill 1
