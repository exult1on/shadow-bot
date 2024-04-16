import json
import discord
import settings
import importlib
from discord import app_commands
from discord.ext import commands

class reverify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_user_menu = app_commands.ContextMenu(name="Reverify user", callback=self.reverify_context_user)

        self.bot.tree.add_command(self.ctx_user_menu)
    
    async def reverify(self, interaction: discord.Interaction, user: discord.Member):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        command_use = "**{0}** requested a re-verify on **{1}**" .format(interaction.user.name, user.name)

        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(user.id)

        if user_id_string in verified:
            verified.pop(user_id_string)

        with open(settings.JSON_DIR, 'w') as json_file:
                json.dump(verified, json_file,
                                    indent=4,
                                    separators=(',',': '))

        verify_channel = interaction.guild.get_channel(settings.Verify_Channel)
        role_verified = interaction.guild.get_role(settings.role_verified)
        role_unverified = interaction.guild.get_role(settings.role_unverified)
        role_ranked = interaction.guild.get_role(settings.role_ranked)

        if role_verified in user.roles:
            await user.remove_roles(role_verified)
        if role_unverified not in user.roles:
            await user.add_roles(role_unverified)
        if role_ranked not in user.roles:
            await user.edit(nick="")

        await verify_channel.send("{0} Please re-verify using the </verify:{1}> command and follow the instructions in the message." .format(user.mention, settings.VerifyCommandID))
        await interaction.response.send_message(content="Requested a re-verify on **{0}**"
                                                .format(user.mention),
                                                ephemeral=True)
        await logs_channel.send(command_use)
    
    @app_commands.command(name = "reverify", description = "Reverify a user with their Roblox account")
    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    @app_commands.describe(user = "The user to request a reverify on")
    async def reverify_command(self, interaction: discord.Interaction, user: discord.Member = None):
        await reverify.reverify(self, interaction, user)

    @app_commands.guilds(settings.ServerID)
    @app_commands.checks.has_role(settings.role_admin)
    async def reverify_context_user(self, interaction: discord.Interaction, user: discord.Member):
        await reverify.reverify(self, interaction, user)

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(reverify(bot))