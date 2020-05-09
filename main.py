# ====================
# Imports
# ====================

# Standard
import asyncio
import datetime
import time
import traceback
from sys import platform

# Community
import discord
from discord.ext import commands
import commentjson as json

# Mine
import Classes.errors as errors
import Classes.commands as bot_commands
import Classes.help_command as help_command
from Classes.UserManager import UserManager
# Functions
from Classes.extra_functions import get_settings_file
from Classes.extra_functions import handleError
from Classes.extra_functions import is_officer
from Classes.extra_functions import check_officer_status


# ====================
# Global Variables
# ====================

if platform == "linux" or platform == "linux2": settings_file_name = "remote_settings"
elif platform == "win32": settings_file_name="test_settings"
settings = get_settings_file(settings_file_name)

bot = commands.Bot(command_prefix=settings["bot_prefix"], help_command=None)

bot.settings = settings
bot.keys = get_settings_file("Keys")

bot.user_manager = UserManager(bot, "vrc_name_db.csv")


# ====================
# Global checks
# ====================

@bot.check
def supports_dms(ctx):
    if ctx.guild is None:
        print("Direct messages not supported.")
        raise commands.NoPrivateMessage("This bot does not support direct messages.")
    else: return True

@bot.check
def is_correct_server(ctx):
    if ctx.guild.id != bot.settings["Server_ID"]:
        raise errors.WrongServer()
    return True


# ====================
# Discord Events
# ====================

@bot.event
async def on_ready():
    print("on_ready")

@bot.event
async def on_message(message):
    print("on_message")

    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    
    officer_before = is_officer(bot, before)
    officer_after = is_officer(bot, after)

    # Member has left the LPD
    if officer_before is True and officer_after is False:
        bot.user_manager.remove_user(before.id)

@bot.event
async def on_error(event, *args, **kwargs):
    print("on_error")
    await handleError(bot, "Error encountered in event: ", event)

@bot.event
async def on_command_error(ctx, exception):
    print("on_command_error")

    exception_string = str(exception).replace("raised an exception", "encountered a problem")
    
    await ctx.send(exception_string)

    if exception_string.find("encountered a problem") != -1:
        err_channel = bot.get_channel(bot.settings["bot_debug_channel"])
        error_string = "***ERROR***\n\n"+exception_string+"\n"+str(traceback.format_exception(None, exception, None))
        error_string.replace("\\n", "\n")# This is still not working
        print(error_string)
        await err_channel.send(error_string)


# ====================
# Add cogs
# ====================

bot.add_cog(bot_commands.VRChatAccoutLink(bot))
bot.add_cog(help_command.Help(bot))


# ====================
# Start
# ====================

bot.loop.create_task(check_officer_status(bot))
bot.run(bot.keys["Discord_token"])