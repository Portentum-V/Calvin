# bot.py
import os
import urllib.request
import subprocess
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SERVERS = os.getenv('MINECRAFT_SERVERS').split(',')

def _currenttime():
    return datetime.datetime.now().strftime('%b %d %H:%M:%S')

bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():

    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{_currenttime()} {bot.user} connected to {guild.name} (id {guild.id})'
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound)):
        # await ctx.message.add_reaction('👀')
        await ctx.message.add_reaction('⁉️')

@bot.command(aliases=['info'])
async def help(ctx):
    help_txt = "Try `@Calvin ip` to get the current IP address or `@Calvin status` to see if the servers are up!\nOr maybe try the secrete command: `@Calvin hobbes`!"
    await ctx.send(help_txt)

@bot.command()
async def ip(ctx):
    httpRequest = urllib.request.urlopen('http://www.icanhazip.org')
    ip_str = httpRequest.read().decode("utf-8").strip()
    await ctx.send(f'Current public IP: `{ip_str}`')

@bot.command(aliases=['status'])
async def mineStats(ctx):
    print('Attempted status check: {0}'.format(_currenttime()))
    serverInfo = []
    for s in SERVERS:
        try:
            output = subprocess.check_output(f"systemctl status {s} -l", shell=True).decode().split('\n')
            status = output[2].strip().split()[1:3]
            command = output[-2]
            serverInfo.append(f"Server `{s}`\n```\nStatus: {' '.join(status)}\nLast log: {command}\n```")
        except Exception as e:
            print(e)
            serverInfo.append(f"Server `{s}` has fallen off the face of the earth.")

    await ctx.send('\n'.join(serverInfo))

@bot.command()
async def hobbes(ctx):
    # httpRequest = urllib.request.urlopen('https://www.gocomics.com/random/calvinandhobbes')
    comic = 'https://www.gocomics.com/random/calvinandhobbes' # Old -> httpRequest.geturl()
    await ctx.send("Calvin and Hobbes go best together!\n" + comic)

bot.run(TOKEN)
