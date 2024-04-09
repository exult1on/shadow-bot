import json
import discord
import settings
from settings import roblox
from discord.ui import View

class Buttons(View):   #!   Buttons
    def __init__(self, discordUser, robloxId, randwords, embed, bot):
        super(Buttons, self).__init__(timeout=None)
        self.discordUser = discordUser
        self.robloxId = robloxId
        self.randwords = randwords
        self.embed = embed
        self.bot = bot

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green, custom_id="done", disabled=True)
    async def done_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)

        roblox_user = await roblox.get_user(self.robloxId)
        button.disabled = True

        if roblox_user.description == self.randwords:
            verified.update({self.discordUser.id: roblox_user.id})
            role_ranked = interaction.guild.get_role(settings.role_ranked)
            role_verified = interaction.guild.get_role(settings.role_verified)
            role_unverified = interaction.guild.get_role(settings.role_unverified)
            if roblox_user.display_name == roblox_user.name:
                verified_name = "{0}" .format(roblox_user.name)
            else:
                verified_name = "{0} (@{1})" .format(roblox_user.display_name, roblox_user.name)

            with open(settings.JSON_DIR, 'w') as json_file:
                json.dump(verified, json_file,
                                    indent=4,
                                    separators=(',',': '))

            self.embed.title="Verification succeeded!"
            self.embed.description="You are now verified with The Shadow"
            self.embed.clear_fields()
            self.embed.color=0x234633
            verdict = "succeded"

            await self.discordUser.remove_roles(role_unverified)
            await self.discordUser.add_roles(role_verified)

            if role_ranked not in self.discordUser.roles:
                await self.discordUser.edit(nick=verified_name)
        else:
            self.embed.title="Verification failed."
            self.embed.description="Please retry the `/verify` command"
            self.embed.clear_fields()
            self.embed.color=0x7b2430
            button.style=discord.ButtonStyle.red
            verdict = "failed"

        await interaction.response.edit_message(view=self, embed=self.embed)
        await logs_channel.send("**{0}**'s verification process has {1}" .format(self.discordUser.name, verdict))