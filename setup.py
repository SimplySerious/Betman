import re
import discord
from datetime import datetime
from time import time, strftime
from readabledelta import readabledelta
import asyncio
yes = ('yes', 'y', 'yar', 'yaar','ye', 'aye', 'ha', 'haan', 'yeah', 'yup','k','ok')
no = ('no', 'n', 'nay', 'na', 'nhi','nahi', 'nah', 'nope')
end = ('end', 'break', 'drop', 'exit', 'bye', 'cancel', 'close')

def addlog(text,client):
    print(ntime(),text)
    if client!=None:
        emb=discord.Embed(description=text,color=discord.Colour.blue())
        emb.timestamp=datetime.utcnow()
        client.loop.create_task(client.logc.send(embed=emb))
def contains_link(message):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.lower())
    if urls:
        return True
    else:
        return False
def ntime():
    return datetime.now().strftime("[%H:%M:%S]")
def dtime(t):
    if t<3600:
        pass
    elif t<43200:#hour
        t=60*(t//60)
    elif t<1036800:#day
        t=3600*(t//3600)
    else:#week
        t=43200*(t//43200)
    return str(readabledelta(seconds=t))

