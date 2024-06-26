import json
import checks
import discord
import settings
import importlib
import uis.exile_modal
from settings import roblox
from roblox import UserNotFound
from discord import app_commands
from discord.ext import commands

class exile(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_user_menu = app_commands.ContextMenu(name="Exile user", callback=self.exile_context_user)

        self.bot.tree.add_command(self.ctx_user_menu)

    async def exile(self, interaction: discord.Interaction, user: discord.Member, roblox_username: str):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        command_use = "**{0}** used the 'exile' command, and" .format(interaction.user.name)
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
            await interaction.response.send_modal(uis.exile_modal.Modal(self.bot, interaction, user, roblox_user))

    @app_commands.command(name = "exile", description = "Exile a user from the group")
    @app_commands.guilds(settings.ServerID)
    @checks.app_check_any(app_commands.checks.has_role(settings.role_admin), app_commands.checks.has_permissions(administrator=True))
    @app_commands.describe(user = "The user to exile", roblox_username = "The Roblox account to exile from the group")
    async def exile_command(self, interaction: discord.Interaction, user: discord.Member = None, roblox_username: str = None):
        await exile.exile(self, interaction, user, roblox_username)

    @app_commands.guilds(settings.ServerID)
    @checks.app_check_any(app_commands.checks.has_role(settings.role_admin), app_commands.checks.has_permissions(administrator=True))
    async def exile_context_user(self, interaction: discord.Interaction, user: discord.Member):
        await exile.exile(self, interaction, user, None)

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(exile(bot))