import json
import words
import random
import discord
import settings
import datetime
from discord.ui import View
from settings import roblox
from discord import app_commands
from roblox.utilities.exceptions import UserNotFound

class Buttons(View):   #!   Buttons
    def __init__(self, discordUser, robloxId, randwords, embed):
        super(Buttons, self).__init__(timeout=None)
        self.discordUser = discordUser
        self.robloxId = robloxId
        self.randwords = randwords
        self.embed = embed

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green, custom_id="done")
    async def done_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        logs_channel = interaction.guild.get_channel(settings.Logs_Channel)
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)

        roblox_user = await roblox.get_user(self.robloxId)
        button.disabled = True

        if roblox_user.description == self.randwords:
            verified.update({self.discordUser.id: roblox_user.id})
            role_unverified = interaction.guild.get_role(settings.role_unverified)
            role_verified = interaction.guild.get_role(settings.role_verified)
            if roblox_user.display_name == roblox_user.name:
                verified_name = "{0}" .format(roblox_user.name)
            else:
                verified_name = "{0} (@{1})" .format(roblox_user.display_name, roblox_user.name)

            with open(settings.JSON_DIR, 'w') as json_file:
                json.dump(verified, json_file,
                                    indent=4,
                                    separators=(',',': '))

            self.embed.title="Verification succeeded!"
            self.embed.description="You are now verified with the Shadow Bot!"
            self.embed.clear_fields()
            self.embed.color=0x234633
            verdict = "succeded"

            await self.discordUser.remove_roles(role_unverified)
            await self.discordUser.add_roles(role_verified)
            # await self.discordUser.edit(nick=verified_name)
        else:
            self.embed.title="Verification failed."
            self.embed.description="Please retry the `/verify` command"
            self.embed.clear_fields()
            self.embed.color=0x7b2430
            button.style=discord.ButtonStyle.red
            verdict = "failed"

        await interaction.response.edit_message(view=self, embed=self.embed)
        await logs_channel.send("**{0}**'s verification process has {1}" .format(self.discordUser.name, verdict))

@app_commands.command(name = "verify", description = "Verify your Roblox account")
@app_commands.guilds(settings.ServerID)
@app_commands.describe(roblox_user = "The username of the account you want to verify with")
async def verify(interaction: discord.Interaction, roblox_user: str):
    logs_channel = interaction.guild.get_channel(settings.Logs_Channel)
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

            view = Buttons(interaction.user, user.id, randwords, embed)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            await logs_channel.send(content="**{0}** started the verification process" .format(interaction.user.name))

        except UserNotFound:
            await interaction.response.send_message(content="Invalid username.", ephemeral=True)
            await logs_channel.send(content="**{0}** tried to start the verification process with an invalid username" .format(interaction.user.name))

async def setup(bot):
    bot.tree.add_command(verify)