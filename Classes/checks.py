# Community
from discord.ext import commands

# Mine
from Classes.extra_functions import is_officer
from Classes.extra_functions import is_higher_up
import Classes.errors as errors

def is_lpd():
    def predicate(ctx):
        if is_officer(ctx.bot, ctx.author) is False:
            raise errors.LPDOnly()
        return True
    return commands.check(predicate)

def is_white_shirt():
    def predicate(ctx):
        if is_higher_up(ctx.bot, ctx.author) is False:
            raise errors.WhiteShirtOnly()
        return True
    return commands.check(predicate)