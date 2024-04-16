import json
import discord
import settings
import importlib
import uis.accept_modal
from settings import roblox
from discord import app_commands
from discord.ext import commands

class accept(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_user_menu = app_commands.ContextMenu(name="Accept user", callback=self.accept_context_user)
        self.ctx_message_menu = app_commands.ContextMenu(name="Accept message", callback=self.accept_context_message)

        self.bot.tree.add_command(self.ctx_user_menu)
        self.bot.tree.add_command(self.ctx_message_menu)

    async def accept(self, interaction: discord.Interaction, user: discord.Member, message: discord.Message):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(user.id)
        group = roblox.get_base_group(settings.GroupID)
        command_use = "**{0}** used the 'accept' command with **{1}**, and they" .format(interaction.user.name, user.name)

        if user_id_string in verified:
            modal = False
            roblox_user = await roblox.get_user(verified[user_id_string])
            roblox_user_roles = await roblox_user.get_group_roles()
            join_request = await group.get_join_request(roblox_user)
            IsIngroup = False

            for isgroup in roblox_user_roles:
                if isgroup.group.id == group.id:
                    IsIngroup = True
                    break

            if IsIngroup == True:
                await interaction.response.send_message(content="User already in the Roblox group", ephemeral=True)
                user_check = "were already in the Roblox group"

            elif join_request == None:
                await interaction.response.send_message(content="No Roblox group join request found", ephemeral=True)
                user_check = "did not send a join request"

            else:
                await interaction.response.send_modal(uis.accept_modal.Modal(self.bot, interaction, user, message, join_request))
                modal = True

            if modal != True:
                await logs_channel.send(" ".join([command_use, user_check]))
        else:
            verify_channel = interaction.guild.get_channel(settings.Verify_Channel)
            role_verified = interaction.guild.get_role(settings.role_verified)
            role_unverified = interaction.guild.get_role(settings.role_unverified)
            user_check = "were not verified, requested a re-verify"

            if role_verified in user.roles:
                await user.remove_roles(role_verified)
            if role_unverified not in user.roles:
                await user.add_roles(role_unverified)
            await user.edit(nick="")

            await verify_channel.send("{0} Please re-verify using the </verify:{1}> command and follow the instructions in the message." .format(user.mention, settings.VerifyCommandID))
            await interaction.response.send_message(content="User is not verified, requested a re-verify", ephemeral=True)
            await logs_channel.send(" ".join([command_use, user_check]))

    @app_commands.command(name = "accept", description = "Accept a verified user into the group")
    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    @app_commands.describe(user = "The user to accept")
    async def accept_command(self, interaction: discord.Interaction, user: discord.Member):
        await accept.accept(self, interaction, user, None)

    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    async def accept_context_user(self, interaction: discord.Interaction, user: discord.Member):
        await accept.accept(self, interaction, user, None)

    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    async def accept_context_message(self, interaction: discord.Interaction, message: discord.Message):
        await accept.accept(self, interaction, message.author, message)

async def setup(bot):
    importlib.reload(uis.accept_modal)
    importlib.reload(settings)
    await bot.add_cog(accept(bot))