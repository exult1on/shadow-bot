import json
import words
import random
import asyncio
import discord
import settings
import datetime
import importlib
import uis.ver_button
from settings import roblox
from discord.ext import commands
from discord import app_commands
from roblox.utilities.exceptions import UserNotFound

class verify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "verify", description = "Verify your Roblox account")
    @app_commands.guilds(settings.ServerID)
    @app_commands.describe(roblox_user = "The username of the account you want to verify with")
    async def verify(self, interaction: discord.Interaction, roblox_user: str):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(interaction.user.id)

        if user_id_string in verified:
            roblox_verified = await roblox.get_user(verified[user_id_string])
            await interaction.response.send_message(content="Already verified with the account of **{0} ({1})**" .format(roblox_verified.name, roblox_verified.id), ephemeral=True)
            await logs_channel.send(content="**{0}** tried to start the verification process while verified"
                                    .format(interaction.user.name))
        else:
            try:
                user = await roblox.get_user_by_username(roblox_user)
                randwords = " ".join(random.choices(words.wordlist, k=10))

                embed = discord.Embed(
                    title="Discord-Roblox veification initiated",
                    description="Hello **{0}**, you started your verification process for the **{1}** account. Please paste the code from the field below into your Roblox account description."
                                .format(interaction.user.display_name, user.name),
                    timestamp=datetime.datetime.now(),
                    color=interaction.user.color)
                embed.add_field(
                    name="**Verification code**",
                    value="`{0}`" .format(randwords))
                embed.set_footer(text="Button will become functional in 15 seconds. Read ^^^")

                view = uis.ver_button.Buttons(interaction.user, user.id, randwords, embed, self.bot)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                await logs_channel.send(content="**{0}** started the verification process" .format(interaction.user.name))
                await asyncio.sleep(15)
                embed.set_footer(text=None)
                view.done_button.disabled = False
                await interaction.edit_original_response(embed=embed, view=view)

            except UserNotFound:
                await interaction.response.send_message(content="Invalid username.", ephemeral=True)
                await logs_channel.send(content="**{0}** tried to start the verification process with an invalid username" .format(interaction.user.name))

async def setup(bot):
    importlib.reload(uis.ver_button)
    importlib.reload(settings)
    await bot.add_cog(verify(bot))