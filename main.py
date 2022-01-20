import asyncio
from concurrent.futures import process
from dataclasses import dataclass
import datetime
from email import message
import functools
import math
from xml.dom.xmlbuilder import Options
from click import option
import discord

from async_timeout import timeout
from discord.ext import commands


class DiscError(Exception):
    pass

class Message(discord.DMChannel):
    discord.message

@classmethod
async def message_channel(self, ctx: commands.Context, write: str, *, loop: asyncio.BaseEventLoop = None):
    loop = loop or asyncio.get_event_loop()

    partial = functools.partial(self.discord.get_input, write, message_channel = True)
    message = await loop.run_in_executor(None, partial)

    if message is None:
        raise DiscError('Please submit something to sell `{}`'.format(write))

    if 'entries' not in message:
        write_info = message
    else:
        write_info = None
        for entry in message['entries']:
            if entry:
                write_info = entry
                break
    if write_info is None:
        raise DiscError('Please submit something to sell `{}`'.format(write))


# when bot is not in use
class inActiveState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.text = None
        

# the acutual bot
class auctioner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.text_state = {}

    # go inactive
    def item_for_sale(self, ctx: commands.Context):
        state = self.text_state.get(ctx.guild.id)
        if not state:
            state = inActiveState(self.bot, ctx)
            self.text_state[ctx.guild,id] = state

        return state

    def cog_check(self, ctx: commands.Context):
        if not ctx.message:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.text_state = self.item_for_sale(ctx)

        # in case of errors
        async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
            await ctx.send('An error has ouccurred: {}'.format(str(error)))

    # @commands.command(name='join', invoke_without_subcommand=True)
    # async def _join(self, ctx: commands.Context):

    #     destination = ctx.author.text.channel
    #     if ctx.text_state.text:
    #         await ctx.text_state.text.move_to(destination)
    #         return
        
    #     ctx.text_state.text = await destination.connect()

    @commands.command(name='sell')
    async def _sell(self, ctx: commands.Context, *, write: str):

            try:
                await Message()
                ctx.send(Message)
            except DiscError as e:
                 await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                message = Message(write)

                await ctx.text_state.text.put(message)





bot = commands.Bot('!', description='Insurgenomics',)
bot.add_cog(auctioner(bot))



@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run('OTMzNTE3MzM0OTEwNTAwOTI0.YeirxA.t77JIVH7fONlEd8SwBrEkpms_2g')