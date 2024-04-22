import discord
import settings
import roblox.users as rbx
from settings import roblox
from roblox import BadRequest
from discord.ext import commands

class Modal(discord.ui.Modal, title="You're about to exile a user"):   #!   Input Field - Modal
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction, user: discord.Member, roblox_user: rbx.User):
        super().__init__()
        self.bot = bot
        self.interaction = interaction
        self.user = user
        self.roblox_user = roblox_user

        if user != None:
            self.add_item(discord.ui.TextInput(label="Please confirm the username of the user.", placeholder=user.name, style=discord.TextStyle.short, max_length=32))
        else:
            self.add_item(discord.ui.TextInput(label="Please confirm the username of the user.", placeholder=roblox_user.name, style=discord.TextStyle.short, max_length=32))

        

    async def on_submit(self, interaction: discord.Interaction):
        if self.children[0].value == self.children[0].placeholder:
            logs_channel = self.bot.get_channel(settings.Logs_Channel)
            await interaction.response.send_message("User found, exiling...", ephemeral=True)

            if self.user != None:
                roles_to_remove = []
                roles_removed = ""
                for role in self.user.roles:
                    if role.id != settings.role_verified and role.name != "@everyone":
                        roles_to_remove.append(role)
                        roles_removed += f"{role.mention} "

                if roles_to_remove:
                    await self.user.remove_roles(*roles_to_remove)

                if self.roblox_user.display_name == self.roblox_user.name:
                    verified_name = "{0}" .format(self.roblox_user.name)
                else:
                    verified_name = "{0} (@{1})" .format(self.roblox_user.display_name, self.roblox_user.name)
                await self.user.edit(nick=verified_name)

            group = await roblox.get_group(settings.GroupID)

            try:
                await group.kick_user(self.roblox_user)
                response = "User properly exiled from the Roblox group"
                verdict = "properly exiled {0} from the Roblox group" .format(self.roblox_user.name)
            except BadRequest:
                response = "User was not in the Roblox group"
                verdict = "the user was not in the Roblox group"

            if self.user != None:
                if roles_to_remove:
                    response += "\nRemoved roles: {0}from the user" .format(roles_removed)
                response += "\nChanged the user's name to their Roblox username"

            await interaction.edit_original_response(content=response)
            await logs_channel.send(content=f"**{self.interaction.user.name}** used the 'exile' command, and {verdict}")
        else:
            await interaction.response.send_message(content="Confirmation failed, user not exiled", ephemeral=True)