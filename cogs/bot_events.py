import json
import discord
import settings
import datetime
from settings import roblox
from discord.ext import commands
from roblox import AvatarThumbnailType
from roblox.utilities.exceptions import BadRequest

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(member.id)
        channel = member.guild.get_channel(settings.ServerMSG_Channel)

        if user_id_string in verified:
            group = await roblox.get_group(settings.GroupID)
            user = await roblox.get_user(verified[user_id_string])

            user_thumbnails = await roblox.thumbnails.get_user_avatar_thumbnails(
                users=[user],
                type=AvatarThumbnailType.headshot,
                size=(420, 420))
            user_thumbnail = user_thumbnails[0]
            
            embed = discord.Embed(
                description="User left, kicked them from the Roblox group",
                timestamp=datetime.datetime.now(),
                color=settings.BootEmbed)
            embed.set_author(
                name=member.display_name,
                url="https://www.roblox.com/users/{0}/profile" .format(user.id),
                icon_url=member.avatar)
            embed.add_field(
                name="‎ ",
                value="**Roblox username:** {0}\n**Roblox account created:** <t:{1}:R> <t:{1}:d>"
                .format(user.name, int(user.created.timestamp())))
            embed.set_thumbnail(
                url=user_thumbnail.image_url)

            try:
                await group.kick_user(user)
                await channel.send(content="{0} left the server." .format(member.mention), embed=embed)

            except BadRequest:
                embed.description = "User left, was not in the Roblox group"
                await channel.send("{0} (outside group) left the server, verification removed." .format(member.mention), embed=embed)

            verified.pop(user_id_string)

            if member.guild.id == settings.ServerID:
                with open(settings.JSON_DIR, 'w') as json_file:
                    json.dump(verified, json_file,
                                        indent=4,
                                        separators=(',',': '))  
        else:
            await channel.send("{0} (unverified) left the server." .format(member.mention))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(settings.ServerMSG_Channel)
        role = discord.utils.get(member.guild.roles, id=settings.role_unverified)

        await member.add_roles(role)
        await channel.send("{0} joined the server" .format(member.mention))

async def setup(bot):
    await bot.add_cog(listeners(bot))