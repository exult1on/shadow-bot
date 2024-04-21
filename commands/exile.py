import json
import discord
import settings
import importlib
from settings import roblox
from roblox import UserNotFound, BadRequest
from discord import app_commands
from discord.ext import commands

class exile(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_user_menu = app_commands.ContextMenu(name="Exile user", callback=self.exile_context_user)

        self.bot.tree.add_command(self.ctx_user_menu)

    async def exile(self, interaction: discord.Interaction, user: discord.Member, roblox_username: str):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        command_use = "**{0}** used the 'exile' command and" .format(interaction.user.name)
        roblox_user = None

        if user != None and roblox_username != None:
            errorMsg = "Command meant to be run with only one parameter"
            verdict = "ran the command with both parameters"

        elif roblox_username == None and user != None:
            with open(settings.JSON_DIR) as f:
                verified = json.load(f)
            user_id_string = str(user.id)

            if user_id_string in verified:
                roblox_user = await roblox.get_user(verified[user_id_string])
            else:
                errorMsg = "User not verified with the Shadow, use the </reverify:{0}> command on the user or try the other parameter" .format(settings.ReverifyCommandID)
                verdict = "the user not verified"

        elif user == None and roblox_username != None:
            try:
                roblox_user = await roblox.get_user_by_username(roblox_username)
            except UserNotFound:
                await interaction.response.send_message(content="Invalid username", ephemeral=True)
                await logs_channel.send(content="{0} chose an invalid username" .format(command_use))
        else:
            errorMsg = "Command can't run with no parameters, you can't exile yourself"
            verdict = "ran the command with no parameters"

        if roblox_user == None:
            await interaction.response.send_message(content=errorMsg, ephemeral=True)
            await logs_channel.send(" " .join([command_use, verdict]))

        else:
            await interaction.response.send_message("User found, exiling...", ephemeral=True)

            if user != None:
                roles_to_remove = []
                roles_removed = ""
                for role in user.roles:
                    if role.id != settings.role_verified and role.name != "@everyone":
                        roles_to_remove.append(role)
                        roles_removed += f"{role.mention} "

                if roles_to_remove:
                    await user.remove_roles(*roles_to_remove)

                if roblox_user.display_name == roblox_user.name:
                    verified_name = "{0}" .format(roblox_user.name)
                else:
                    verified_name = "{0} (@{1})" .format(roblox_user.display_name, roblox_user.name)
                await user.edit(nick=verified_name)

            group = await roblox.get_group(settings.GroupID)

            try:
                await group.kick_user(roblox_user)
                response = "User properly exiled from the Roblox group"
                verdict = "properly exiled {0} from the Roblox group" .format(roblox_user.name)
            except BadRequest:
                response = "User was not in the Roblox group"
                verdict = "the user was not in the Roblox group"

            if user != None:
                if roles_to_remove:
                    response += "\nRemoved roles: {0}from the user" .format(roles_removed)
                response += "\nChanged the user's name to their Roblox username"

            await interaction.edit_original_response(content=response)
            await logs_channel.send(" " .join([command_use, verdict]))

    @app_commands.command(name = "exile", description = "Exile a user from the group")
    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    @app_commands.describe(user = "The user to exile", roblox_username = "The Roblox account to exile from the group")
    async def exile_command(self, interaction: discord.Interaction, user: discord.Member = None, roblox_username: str = None):
        await exile.exile(self, interaction, user, roblox_username)

    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    async def exile_context_user(self, interaction: discord.Interaction, user: discord.Member):
        await exile.exile(self, interaction, user, None)

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(exile(bot))