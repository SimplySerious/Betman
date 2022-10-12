from discord.ext import commands
import re
import random
class DadJokes(commands.Cog):
	"""From the makers of DadBot (not really), I present to you, DadJokes (wait, why would the makers make a thing they already made? ykw? This was cringe, ngl).
	You might ask, Where are the commands of This module? Well you see, This module consists only on_message. soo no commands for ya.
	Also, Congrats on finding this Message"""
	def __init__(self, client):
		self.client = client
			
	@commands.Cog.listener()
	async def on_message(self,msg):
		if not msg.author.bot and len(msg.content)!=0 and msg.content[0]!='=':
			dadl = re.match("(.*\s)?(im|i'm|i am)\s(.*)", msg.content, re.IGNORECASE)
			if random.choice((True,True)) and self.client.user != msg.author and dadl and len(dadl.group(3))<20:
				if msg.guild.me.nick == None:
					myname = self.client.user.name
				else:
					myname = msg.guild.me.nick
				
				if dadl.group(3).lower() in ("joe","dad","daddy","father","papa","god","bhagvan"):
					await msg.reply(f"Hi {msg.author.mention}, you are not {dadl.group(2)}")
				elif dadl.group(3).lower() in (myname.lower(),"batman","batman bot", "batmanbot"):
					await msg.reply(f"No ***in deep voice***, {dadl.group(2)} {dadl.group(3)}")
				elif dadl.group(3).lower() == "thugesh":
					if msg.author.id != 769556818674188300:
						await msg.reply(f"Hi {msg.author.mention}, you are not Thugesh")
					else:
						await msg.reply(f"Hi {msg.author.mention}, you are indeed Thugesh")
				else:
					await msg.reply(f"Hi '{dadl.group(3)}', {dadl.group(2)} {myname}")
			elif msg.content=='69':
				await msg.reply(random.choice(('Nice','Reddit-Moment')))
			elif msg.content[:4].lower()=='oho ':
				await msg.reply("My prefix has been changed from `oho (command_name)` to `b (command_name)`.\nPlease use the new prefix instead.")
			elif msg.content[:4].lower()=='?afk' or msg.content[:4].lower()=='*afk':
				await msg.reply("How bout You use me instead? :flushed:\nJust use `b afk [your_text_here]`")
			elif msg.content.lower()=='ping':
				await msg.reply(f'Pong! `{round(self.client.latency * 1000)}ms`')
			elif msg.content.lower() in ('lag','lag?'):
				await msg.reply('No')
			elif msg.content.lower() == "ding":
				await msg.reply("Dong")
			elif msg.content.lower() == "ching":
				await msg.reply(random.choice(["Chong","Eww Racist"]))
			elif msg.content in (f'<@{self.client.user.id}>', f'<@!{self.client.user.id}>'):
				await msg.reply(f"My prefix is {','.join(item for item in self.client.command_prefix)}")
			else:
				pass
