# Standard
from io import StringIO
from io import BytesIO

# Community
import discord
from discord.ext import commands
from discord.ext import menus

# Mine
import Classes.errors as errors
import Classes.UserManager
import Classes.menus as my_menus
import Classes.checks as checks
from Classes.extra_functions import send_long_str

class VRChatAccoutLink(commands.Cog):
    """This stores all the VRChatAccoutLink commands."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @checks.is_lpd()
    @checks.is_general_bot_channel()
    async def info(self, ctx):
        """
        This command gets info about your current account status.

        This command shows you information about if you have your VRChat account connected or
        not and how to connect it or disconnect it.
        """
        vrchat_name = self.bot.user_manager.get_vrc_by_discord(ctx.author.id)
        if vrchat_name:
            await ctx.send(f'You have a VRChat account linked with the name `"{vrchat_name}"`, if you want to unlink it use the command $unlink or if you want to update your VRChat name use the command $link new_vrchat_name.')
        else:
            await ctx.send("You do not have a VRChat account linked, to connect your VRChat account do $link your_vrchat_name.")

    @commands.command()
    @checks.is_lpd()
    @checks.is_general_bot_channel()
    async def link(self, ctx, vrchat_name):
        r"""
        This command is used to tell the bot your VRChat name.

        This information is used for detecting if you are in
        the LPD when entering the LPD Station. To use the
        command do $link your_vrchat_name.

        If your VRChat name contains spaces put quotes before and after
        your VRChat name, example: $link "your vrchat name". If it contains
        quotes and spaces you can do \ before every quote you want to be
        apart of your name, example: $link "your \\\"vrchat\\\" name".
        """

        # Make sure the name does not contain the seperation character
        if self.bot.settings["name_separator"] in vrchat_name:
            hroi = self.bot.get_guild(self.bot.settings["Server_ID"]).get_member(378666988412731404)
            await ctx.send(f'The name you put in contains a character that cannot be used "{self.bot.settings["name_separator"]}" please change your name or contact {hroi.mention} so that he can change the illegal character.')
            return

        # If the officer already has a registered account
        previous_vrchat_name = self.bot.user_manager.get_vrc_by_discord(ctx.author.id)
        if previous_vrchat_name:
            confirm = await my_menus.Confirm(f'You already have a VRChat account registered witch is `"{previous_vrchat_name}"`, do you want to replace that account?').prompt(ctx)
            if not confirm:
                await ctx.send("Your account linking has been cancelled, if you did not intend to cancel the linking you can use the command $link again.")
                return

        # Confirm the VRC name
        confirm = await my_menus.Confirm(f'Are you sure `"{vrchat_name}"` is your full VRChat name?\n**You will be held responsible of the actions of the VRChat user with this name.**').prompt(ctx)
        if confirm:
            self.bot.user_manager.add_user(ctx.author.id, vrchat_name)
            await ctx.send(f'Your VRChat name has been set to `"{vrchat_name}"`\nIf you want to unlink it you can use the command $unlink')
        else:
            await ctx.send("Your account linking has been cancelled, if you did not intend to cancel the linking you can use the command $link again.")
    
    @commands.command()
    @checks.is_lpd()
    @checks.is_general_bot_channel()
    async def unlink(self, ctx):
        """
        This command removes your account if you have a
        connected VRChat account.
        """
        vrchat_name = self.bot.user_manager.get_vrc_by_discord(ctx.author.id)

        if vrchat_name == None:
            await ctx.send("You do not have your VRChat name linked.")
            return

        confirm = await my_menus.Confirm(f'Your VRChat name is currently set to `"{vrchat_name}"`. Do you want to unlink that?').prompt(ctx)
        if confirm:
            self.bot.user_manager.remove_user(ctx.author.id)
            await ctx.send('Your VRChat name has been successfully unlinked, if you want to link another account you can do that with $link.')
        else:
            await ctx.send(f'Your VRChat accout has not been unlinked and is still `"{vrchat_name}"`')
    
    @commands.command()
    @checks.is_white_shirt()
    @checks.is_admin_bot_channel()
    async def list_vrc_names(self, ctx):
        """
        This command is used to get the VRChat names of the people that are LPD Officers.
        
        The output from this command is only intended to be read by computers and is not
        easy to read for humans.
        """
        sep_char = self.bot.settings["name_separator"]
        vrc_names = [x[1] for x in self.bot.user_manager.all_users]
        
        output_text = f"{sep_char.join(vrc_names)}"
        if len(output_text) < 2000:
            await ctx.send(output_text)
        else:
            with StringIO(output_text) as error_file_sio:
                with BytesIO(error_file_sio.read().encode('utf8')) as error_file:
                    await ctx.send("The output is too big to fit in a discord message so it is insted in a file.", file=discord.File(error_file, filename="all_vrc_names.txt"))

    @commands.command()
    @checks.is_white_shirt()
    @checks.is_admin_bot_channel()
    async def list_all(self, ctx):
        """
        This command shows the Discord and VRChat names of all officers registered with the bot.

        This information is intended to check who has a specific VRChat account.
        """
        out_string = "**All linked accounts:**\n**Discord - VRChat\n**"

        guild = self.bot.get_guild(self.bot.settings["Server_ID"])
        for user in self.bot.user_manager.all_users:
            member = guild.get_member(user[0])
            string_being_added = f"`{member.display_name} - {user[1]}`\n"

            if len(out_string + string_being_added) >= 2000:
                await ctx.send(out_string)
                out_string = string_being_added
            else:
                out_string += string_being_added
        await ctx.send(out_string)

    @commands.command()
    @checks.is_white_shirt()
    @checks.is_admin_bot_channel()
    async def debug(self, ctx):
        """
        This command is just for testing the bot.
        """
        await ctx.send(str(self.bot.user_manager.all_users))

class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def filter_start_end(string, list_of_characters_to_filter):
        while True:
            if string[0] in list_of_characters_to_filter:
                string = string[1::]
            else: break

        while True:
            if string[-1] in list_of_characters_to_filter:
                string = string[0:-1]
            else: break
        
        return string


    @commands.command()
    @checks.is_white_shirt()
    @checks.is_admin_bot_channel()
    async def vrc_names_in_role(self, ctx, role_name):

        # Get the role
        return_role = None
        for role_2 in ctx.guild.roles:
            if self.filter_start_end(role_2.name, ["|", " ", "⠀", " "]) == role_name:
                return_role = role_2
                break
        
        # Make sure the role was found and that people have it
        if return_role == None:
            await ctx.send(f"The role {role_name} does not exist.")
            return
        if not return_role.members:
            await ctx.send(f"{role_name} is empty")
            return
        
        # Send everyone
        send_str = f"Here is everyone in the role {role_name}:\n"
        send_str += "```" + "\n".join(self.bot.user_manager.get_vrc_by_discord(x.id) or x.display_name for x in return_role.members) + "```"

        await send_long_str(ctx, send_str)