import json
import discord
import datetime
import settings
import importlib
from settings import roblox
from discord import app_commands
from discord.ext import commands
from roblox import UserNotFound, AvatarThumbnailType

class bgcheck(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_user_menu = app_commands.ContextMenu(name="Run bgcheck", callback=self.bgcheck_context_user)

        self.bot.tree.add_command(self.ctx_user_menu)

    async def bgcheck(self, interaction: discord.Interaction, user: discord.Member, roblox_username: str):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        command_use = "**{0}** used the 'bgcheck' command and" .format(interaction.user.name)
        roblox_user = None
        if user != None and roblox_username != None:
            errorMsg = "Command meant to be run with only one parameter"
            verdict = "ran the command with both parameters"

        elif user == None and roblox_username != None:
            try:
                roblox_user = await roblox.get_user_by_username(roblox_username)
            except UserNotFound:
                await interaction.response.send_message(content="Invalid username", ephemeral=True)
                await logs_channel.send(content="{0} chose an invalid username" .format(command_use))
        else:
            if user == None and roblox_username == None:
                user = interaction.user

            with open(settings.JSON_DIR) as f:
                verified = json.load(f)
            user_id_string = str(user.id)

            if user_id_string in verified:
                roblox_user = await roblox.get_user(verified[user_id_string])
            else:
                if user == interaction.user:
                    errorMsg = "You're not verified, try to run </verify:{0}> to use this command on yourself" .format(settings.VerifyCommandID)
                else:
                    errorMsg = "User not verified with The Shadow, try the other parameter"
                verdict = "the user was not verified"

        if roblox_user == None:
            await interaction.response.send_message(content=errorMsg, ephemeral=True)
            await logs_channel.send(" " .join([command_use, verdict]))
        else:
            badgeIds = [2126481824, 2126481811, 2126481836, 2126481832, 2126481850, 2126481842, 2126481859, 2126481853, 2126482039, 2126482036, 2126482050, 2126482046]
            badgesList = []
            for index in badgeIds:
                badge = roblox.get_base_badge(index)
                badgesList.append(badge)

            for i in range(2):
                badgeInfo = await roblox_user.get_badge_awarded_dates(badgesList)

            user_thumbnails = await roblox.thumbnails.get_user_avatar_thumbnails(
                users=[roblox_user],
                type=AvatarThumbnailType.headshot,
                size=(420, 420))
            user_thumbnail = user_thumbnails[0]

            embed = discord.Embed(
                title=roblox_user.name,
                description="Information about user",
                url="https://www.roblox.com/users/{0}/profile" .format(roblox_user.id),
                timestamp=datetime.datetime.now(),
                color=interaction.user.color)
            embed.set_thumbnail(url=user_thumbnail.image_url)

            friend_count = await roblox_user.get_friend_count()
            follower_count = await roblox_user.get_follower_count()
            following_count = await roblox_user.get_following_count()

            embed.add_field(name="Join Date", value="<t:{0}:F> <t:{0}:R>" .format(int(roblox_user.created.timestamp())), inline=False)
            embed.add_field(name="Friends", value=friend_count, inline=True)
            embed.add_field(name="Followers", value=follower_count, inline=True)
            embed.add_field(name="Following", value=following_count, inline=True)

            woodworking = "❌"
            woodcutting = "❌"
            smithing = "❌"
            mining = "❌"
            leatherworking = "❌"
            hunting = "❌"

            for badge in badgeInfo:
                if badge.id == 2126481824:
                    woodworking = "✅"
                elif badge.id == 2126481811:
                    woodworking = "⭐"
                elif badge.id == 2126481836:
                    woodcutting = "✅"
                elif badge.id == 2126481832:
                    woodcutting = "⭐"
                elif badge.id == 2126481850:
                    smithing = "✅"
                elif badge.id == 2126481842:
                    smithing = "⭐"
                elif badge.id == 2126481859:
                    mining = "✅"
                elif badge.id == 2126481853:
                    mining = "⭐"
                elif badge.id == 2126482039:
                    leatherworking = "✅"
                elif badge.id == 2126482036:
                    leatherworking = "⭐"
                elif badge.id == 2126482050:
                    hunting = "✅"
                elif badge.id == 2126482046:
                    hunting = "⭐"

            embed.add_field(
                name="Professions",
                value="Woodworking - {0}\nWoodcutting - {1}\nSmithing - {2}\nMining - {3}\nLeatherworking - {4}\nHunting - {5}"
                    .format(woodworking, woodcutting, smithing, mining, leatherworking, hunting),
                inline=True)
            embed.add_field(name="Legend", value="✅ - Adept and up\n⭐ - Master\n❌ - Apprentice and below", inline=True)
            embed.set_footer(text=f"{interaction.user.name} has marked him for death", icon_url=interaction.user.avatar)

            verdict = "fetched the stats for **{0}**" .format(roblox_user.name)
            await logs_channel.send(" " .join([command_use, verdict]))
            if interaction.channel_id == settings.Bot_Channel:
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name = "bgcheck", description = "Provides a background check on a Roblox user")
    @app_commands.guilds(settings.ServerID)
    @app_commands.describe(user = "Request a background check on a VERIFIED Discord user", roblox_username = "Request a background check on a Roblox user")
    async def bgcheck_command(self, interaction: discord.Interaction, user: discord.Member = None, roblox_username: str = None):
        await bgcheck.bgcheck(self, interaction, user, roblox_username)

    @app_commands.guilds(settings.ServerID)
    async def bgcheck_context_user(self, interaction: discord.Interaction, user: discord.Member):
        await bgcheck.bgcheck(self, interaction, user, None)

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(bgcheck(bot))