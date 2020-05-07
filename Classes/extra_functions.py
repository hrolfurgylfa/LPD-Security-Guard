# Standard
import traceback

# Community
import discord
from discord.ext import commands
import commentjson as json

def get_settings_file(settings_file_name, in_settings_folder = True):
    
    # Add the stuff to the settings_file_name to make it link to the right file
    file_name = settings_file_name+".json"

    # Add the settings folder to the filename if necessary
    if in_settings_folder: file_name = "settings/" + file_name

    # Get all the data out of the JSON file, parse it and return it
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data

async def handleError(bot, *text, end=" "):
    error_text = "***ERROR***\n\n"
    for line in text: error_text += str(line) + end
    error_text += "\n" + traceback.format_exc()

    print(error_text)

    channel = bot.get_channel(bot.settings["bot_debug_channel"])
    try:
        await channel.send(error_text)
    except discord.InvalidArgument:
        await channel.send("***I ENCOUNTERED AN ERROR AND THE ERROR MESSAGE DOES NOT FIT IN DISCORD.***")

def is_officer(bot, member):
    if member is None: return False

    officer_roles = [x["id"] for x in bot.settings["role_ladder"] if x["name_id"] != "cadet"]
    for role in member.roles:
        if role.id in officer_roles:
            return True
    return False

def is_higher_up(bot, member):
    if member is None: return False

    white_shirt_roles = [x["id"] for x in bot.settings["role_ladder"] if "is_white_shirt" in x and x["is_white_shirt"] == True]
    for role in member.roles:
        if role.id in white_shirt_roles:
            return True
    return False