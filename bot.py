#!/usr/bin/python3
# coding=utf-8

# print imports
import asyncio
import time
import codecs
import pip
import sys

# custom Imports
import discord
from discord.ext import commands
from discord.utils import get
from colorama import *
import youtube_dl

#import test


def time_HMS():
    return str(time.strftime("%H:%M:%S"))


def time_date():
    return str(time.strftime("%d.%m.%Y"))


def log(message, log_type="INFO", log_file="bot.log"):
    log_types = {
        "INFO": Style.BRIGHT + Fore.WHITE,
        "DEBUG": Style.BRIGHT + Fore.YELLOW,
        "WARNING": Style.BRIGHT + Fore.RED,
        "ERROR": Style.DIM + Fore.RED,
    }
    message = '[' + time_date() + " " + time_HMS() + " " + str(log_type) + "]: " + str(message)

    with codecs.open(log_file, "a", "utf-8") as log_file:
        log_file.write(message + "\n")
        log_file.close()

    print(log_types[log_type] + message)


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes

}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music_bot(object):
    def __init__(self, token, prefix):
        self.prefix = prefix
        self.bot = commands.Bot(self.prefix)
        self.bot.remove_command('help')
        self.token = token
        self.owner = 664875548358606878

#Start gui print
    def run(self):
        @self.bot.event
        async def on_ready():
            init()
            print(Fore.GREEN + Style.BRIGHT)
            print("║ Bot Start um :" + str(time_HMS()) + " am " + str(time_date()) + "")
            print("║ Bot Name " + str(self.bot.user.name) + '#' + str(self.bot.user.discriminator) + "")
            print("║ Bot Version ""2.0.1")
            print("║ Bot ID " + str(self.bot.user.id) + "")
            print("║ pip Version {}".format(str(pip.__version__)))
            print("║ Discord Version " + str(discord.__version__) + "")
            print("║ Pyton.version {}".format(str(sys.version.split()[0])))
            print("║ Bot Upgrate vom 24.1.2020 / Bot 2.0.1")
            init()
            print(Style.RESET_ALL + "\n")

        @self.bot.command()
        async def YouTube(ctx):
            embed = discord.Embed(
                color= 0x0ff
            )

            embed.set_author(name='Commands')
            embed.add_field(name=self.prefix + 'help', value='Scripting by [NIKI FOX](https://www.youtube.com/channel/UC5UKaDtjhgze9Dow_VT3d4w) & [Commandcracker](https://www.youtube.com/channel/UC5UKaDtjhgze9Dow_VT3d4w)', inline=False)
            embed.add_field(name=self.prefix + 'NIKI FOX', value='Play a song', inline=False)

            await ctx.send(embed=embed)

        @self.bot.command()
        async def help(ctx):
            embed = discord.Embed(
                color= 0x0080ff
            )

            embed.set_author(name='Commands')
            embed.add_field(name=self.prefix + 'help', value='Shows this message', inline=False)
            embed.add_field(name=self.prefix + 'play', value='Play a song', inline=False)
            embed.add_field(name=self.prefix + 'join', value='Make the bot join the cahannel', inline=False)
            embed.add_field(name=self.prefix + 'leave', value='Make the bot leave the cahannel', inline=False)
            embed.add_field(name=self.prefix + 'stop', value='Meakes the bot stop the song', inline=False)
            embed.add_field(name=self.prefix + 'volume', value='set the music volume', inline=False)
            embed.add_field(name=self.prefix + 'pause', value='pause the music', inline=False)
            embed.add_field(name=self.prefix + 'resume', value='resume the music', inline=False)
            embed.add_field(name=self.prefix + ' ', value='' + str(time_HMS()) + " am " + str(time_date()) + '', inline=False)

            await ctx.send(embed=embed)


        @self.bot.command(pass_context=True, aliases=['j', 'joi'])
        async def join(ctx):
            if not ctx.message.author.voice:
                await ctx.send(":x: **You have to be in a voice channel**")
            else:
                channel = ctx.message.author.voice.channel
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected and voice.channel == channel:
                    await ctx.send(":x: **I am arealy in your voice channel**")
                else:
                    if voice and voice.is_connected:
                        await voice.move_to(channel)
                    else:
                        await channel.connect()
                    await ctx.send(":white_check_mark: **Joined**")

        @self.bot.command(pass_context=True)
        async def leave(ctx):
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected:
                await voice.disconnect()
                await ctx.send(":white_check_mark: **Disconnected**")
            else:
                await ctx.send(":x: **I am not connected to a voice channel**")

        @self.bot.command(pass_context=True)
        async def play(ctx, *, url):
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            # join and already playing Check
            if not (voice and voice.is_connected):
                if not ctx.message.author.voice:
                    await ctx.send(":x: **You have to be in a voice channel**")
                    return
                else:
                    channel = ctx.message.author.voice.channel
                    await channel.connect()
            elif voice.is_playing():
                await ctx.send(":x: **im already playing**")
                return

            msg = await ctx.send("**Searching** :mag_right: ``" + url + "``")

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await msg.edit(content="**Playing** :notes: ``" + str(player.title) + "``")

        @self.bot.command(pass_context=True)
        async def volume(ctx, volume: int):

            if ctx.voice_client is None:
                await ctx.send(":x: **Not connected to a voice channel.**")

            ctx.voice_client.source.volume = volume / 100
            await ctx.send(":white_check_mark: **Changed volume to " + str(volume) + "%**")

        @self.bot.command(pass_context=True)
        async def stop(ctx):
            if not (ctx.voice_client and ctx.voice_client.is_playing()):
                await ctx.send(":x: **There is nothing to stop**")
            else:
                ctx.voice_client.stop()
                await ctx.send(":white_check_mark: **Stoped playing**")

        @self.bot.command(pass_context=True)
        async def pause(ctx):
            if not (ctx.voice_client and ctx.voice_client.is_playing()):
                await ctx.send(":x: **There is nothing to pause**")
            else:
                ctx.voice_client.pause()
                await ctx.send(":white_check_mark: **Paused**")
#------------------------------------------------------------------------

        @self.bot.command()
        async def prefix(ctx):
            await ctx.send('Der Bot Prefix ist `""`')

# ------------------------------------------------------------------------

        @self.bot.command()
        async def say(ctx):
            await ctx.send('https://images2.weku.io/DQmPNCiE3eEM973mtWvSHJXtSbLHAywFQ8qZZeuokHrbRgs/discordjoin%20gif.gif')

# ------------------------------------------------------------------------

        @self.bot.command(pass_context=True)
        async def inf(ctx):
            await ctx.send('https://cdn.discordapp.com/attachments/665213881551028246/665213882146619395/rainbow.gif')
            await ctx.send('https://fontmeme.com/temporary/cff112bde14f14b4e5d4d2b2c57fd0f9.png')
            await ctx.send('https://cdn.discordapp.com/attachments/665213881551028246/665213882146619395/rainbow.gif')

#------------------------------------------------------------------------

        @self.bot.command()
        async def tta(ctx):
            embed = discord.Embed(
                color= 0x0080ff
            )

            embed.set_author(name='e')
            embed.set_image(url='https://fontmeme.com/permalink/200215/4526e51c9dbb17e88e57854227c919f5.png https://fontmeme.com/temporary/cff112bde14f14b4e5d4d2b2c57fd0f9.png')
            embed.add_field(name='play', value='Play a song', inline=False)

            await ctx.send(embed=embed)

# ------------------------------------------------------------------------
        @self.bot.command(pass_context=True)
        async def trt(ctx):
            await ctx.send('https://steemitimages.com/DQmWXUDVSUZBTUbwNPBvqoi44rBtTrE3E9xeGYSkV6P1rQY/D.Bot.png')

# ------------------------------------------------------------------------


        @self.bot.command()
        async def ui(ctx):
            embed = discord.Embed(
                color= 0x0080ff
            )

            embed.set_author(name='USER INFO {0.author.mention} '.format(message))
            embed.add_field(name=self.prefix + 'help', value='öööö', inline=False)
            embed.add_field(name=self.prefix + 'play', value='Play a song', inline=False)
            embed.add_field(name=self.prefix + 'join', value='Make the bot join the cahannel', inline=False)
            embed.add_field(name=self.prefix + 'leave', value='Make the bot leave the cahannel', inline=False)
            embed.add_field(name=self.prefix + 'stop', value='Meakes the bot stop the song', inline=False)
            embed.add_field(name=self.prefix + 'volume', value='set the music volume', inline=False)
            embed.add_field(name=self.prefix + 'pause', value='pause the music', inline=False)
            embed.add_field(name=self.prefix + 'resume', value='resume the music', inline=False)
            embed.add_field(name=self.prefix + ' ', value='' + str(time_HMS()) + " am " + str(time_date()) + '', inline=False)

            await ctx.send(embed=embed)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
        @self.bot.command()
        async def myinfo(ctx):
            await ctx.send('**USER INFO**\nUser name: {0.author.mention}\nUser #id: #{0.author.discriminator}\nUser id: {0.author.id}\n------------ '.format(ctx))
#------------------------------------------------------------------------
#------------------------------------------------------------------------
        @self.bot.command()
        async def userinfo(ctx):
            embed = discord.Embed(
                color=0x0080ff
            )

            embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_author(name='USER INFO')
            embed.set_thumbnail(url="https://www.wurst-paket.de/media/image/f7/60/47/ximage_103633_1_600x600.jpg.pagespeed.ic.VrfGfsvjhj.jpg")
            embed.add_field(name=self.prefix + '-', value='ll', inline=False)
            embed.add_field(name=self.prefix + '-', value='[YouTube](https://www.youtube.com/)', inline=False)
            embed.add_field(name=self.prefix + '-', value='[Live kounter](https://livecounts.net/)', inline=False)
            embed.add_field(name=self.prefix + '-', value='[stream laps](https://streamlabs.com/)', inline=False)
            embed.add_field(name=self.prefix + '-', value='[OBS](https://obsproject.com/de)', inline=False)
            embed.add_field(name=self.prefix + '-', value='' + str(time_HMS()) + " am " + str(time_date()) + '',inline=False)

            await ctx.send(embed=embed)

# ------------------------------------------------------------------------

        @self.bot.command(pass_context=True)
        async def ping(ctx):
            time_then = time.monotonic()
            pinger = await ctx.send(':\n**SERVER** Pinging Test...')
            ping = '%.2f' % (1000 * (time.monotonic() - time_then))
            await pinger.edit(content=':\n**SERVER** Pinging Test Successful :white_check_mark:\n:\n**SERVER** Ping ▶ **' + str(round(int(float(ping)))) + 'ms** ◀\n:\n**SERVER** Pinging Test Successful :white_check_mark:')

        @self.bot.command()
        async def clear(ctx, number):
            global deleted
            if ctx.message.author.id == self.owner:
                try:
                    number = int(number)
                except ValueError:
                    try:
                        await ctx.send(":x: **ERROR**```diff\n-Sie müssen eine Nummer eingeben```")
                    except discord.Forbidden:
                        try:
                            await ctx.message.author.send("**I don't have permission to send messages**")
                        except discord.Forbidden:
                            pass
                else:
                    if number <= 0 or number > 100:
                        embed = discord.Embed(color=discord.Color.red())

                        embed.add_field(name="max", value="1000", inline=True)
                        embed.add_field(name="min", value="1", inline=True)

                        try:
                            await ctx.send(embed=embed)
                        except discord.Forbidden:
                            try:
                                await ctx.message.author.send("**I don't have permission to send messages**")
                            except discord.Forbidden:
                                pass
                    else:
                        try:
                            await ctx.message.delete()
                            deleted = await ctx.channel.purge(limit=number)
                        except discord.Forbidden:
                            try:
                                await ctx.message.author.send("``◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥``:warning:\n:x: **ERROR** ```diff\n-Ich habe keine Berechtigung zum Löschen von Nachrichten```:x: **ERROR**\n``◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥``:warning:")
                            except discord.Forbidden:
                                pass
                            return

                        embed = discord.Embed(title='Deleted {} message(s)'.format(len(deleted)),
                                              color=discord.Color.red())

                        try:
                            await ctx.channel.send(delete_after=3, embed=embed)
                        except discord.Forbidden:
                            try:
                                await ctx.message.author.send("``◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥``:warning:\n:x: **ERROR** ```diff\n-Ich habe keine Berechtigung zum Senden von Nachrichten```:x: **ERROR**\n``◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥``:warning:")
                            except discord.Forbidden:
                                pass

        @clear.error
        async def clear_handler(ctx, error):
            if ctx.message.author.id == self.owner:
                if isinstance(error, commands.MissingRequiredArgument):
                    try:
                        await ctx.send(":x: **ERROR**\nSie müssen nach dem Befehl einen Wert eingeben zwischen 1 und 1000!")
                    except discord.Forbidden:
                        try:
                            await ctx.message.author.send(":x: **ERROR**\nIch habe keine Berechtigung zum Senden von Nachrichten!")
                        except discord.Forbidden:
                            pass
                    return

                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


        @self.bot.command(pass_context=True)
        async def resume(ctx):
            if not (ctx.voice_client and ctx.voice_client.is_paused()):
                await ctx.send(":x: **There is nothing to resume**")
            else:
                ctx.voice_client.resume()
                await ctx.send(":white_check_mark: **Resumed**")

        self.bot.run(self.token)

# run
if __name__ == '__main__':
    prefix = '""'
    token = open(r'token.txt', 'r').read()
    Music_bot(token, prefix).run()
