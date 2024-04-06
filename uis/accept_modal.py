import discord
import settings
from discord.ext import commands

class Modal(discord.ui.Modal, title="Accepting"):   #!   Input Field - Modal
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction, user: discord.User, message: discord.Message, join_request):
        super().__init__()
        self.bot = bot
        self.interaction = interaction
        self.user = user
        self.message = message
        self.join_request = join_request

    charName = discord.ui.TextInput(label="Character name of the user", placeholder="Name and surname (NO DETACHMENT TAG)", style=discord.TextStyle.short, max_length=32)

    async def on_submit(self, interaction: discord.Interaction):
        await self.join_request.accept()
        WelcomeChannel = self.bot.get_channel(settings.Welcome_Channel)
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        if self.message != None:
            emoji = self.bot.get_emoji(settings.AcceptEmoji)
            await self.message.add_reaction(emoji)

        AcceptRoles = []
        for roles in settings.AcceptRoles:
            role = self.interaction.guild.get_role(roles)
            AcceptRoles.append(role)

        await self.user.add_roles(*AcceptRoles)
        await self.user.edit(nick=f"[B] {str(self.charName).title()}")
        await interaction.response.send_message(content="User accepted succesfully", ephemeral=True)
        await WelcomeChannel.send(content="{0} Welcome to The Shadow Forces!" .format(self.user.mention))
        await logs_channel.send(content="**{0}** used the 'accept' command with **{1}**, and they were accepted into the Roblox group"
                                .format(interaction.user.name, self.user.name))