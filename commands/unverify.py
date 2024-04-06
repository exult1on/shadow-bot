import json
import discord
import settings
from discord.ext import commands
from discord import app_commands

class unverify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "unverify", description = "Unverify your Roblox account")
    @app_commands.guilds(settings.ServerID)
    async def unverify(self, interaction: discord.Interaction):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(interaction.user.id)

        if user_id_string in verified:
            role_verified = interaction.guild.get_role(settings.role_verified)
            role_unverified = interaction.guild.get_role(settings.role_unverified)

            verified.pop(user_id_string)

            await interaction.user.remove_roles(role_verified)
            await interaction.user.add_roles(role_unverified)
            await interaction.user.edit(nick="")
            await interaction.response.send_message(content="Verification removed properly", ephemeral=True)
            await logs_channel.send(content="**{0}** tried to use the 'unverified' command and their verification was removed" .format(interaction.user.name))

            with open(settings.JSON_DIR, 'w') as json_file:
                json.dump(verified, json_file,
                                    indent=4,
                                    separators=(',',': '))
        else:
            await interaction.response.send_message(content="You can't unverify if you're not verified, use the </verify:{0}> command to verify" .format(settings.VerifyCommandID), ephemeral=True)
            await logs_channel.send(content="**{0}** tried to use the 'unverified' command and they were not verified" .format(interaction.user.name))

async def setup(bot):
    await bot.add_cog(unverify(bot))