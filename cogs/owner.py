import json
import discord
import settings
import importlib
from discord.ext import commands

def guildcheck(ctx):
    return ctx.guild.id == settings.ServerID

class owner(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    @commands.check(guildcheck)
    async def forcever(self, ctx: commands.Context, discordid: int, robloxid: int):
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(discordid)

        if user_id_string in verified:
            await ctx.send("User already verified")
        else:
            verified.update({discordid: robloxid})
        
            with open(settings.JSON_DIR, 'w') as json_file:
                    json.dump(verified, json_file,
                                        indent=4,
                                        separators=(',',': '))
            
            await ctx.send("User verification added properly")

    @commands.command()
    @commands.is_owner()
    @commands.check(guildcheck)
    async def forceunver(self, ctx: commands.Context, discordid: int):
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(discordid)

        if user_id_string not in verified:
            await ctx.send("User not verified")
        else:
            verified.pop(user_id_string)

            with open(settings.JSON_DIR, 'w') as json_file:
                    json.dump(verified, json_file,
                                        indent=4,
                                        separators=(',',': '))

            await ctx.send("User unverification removed properly")

    @commands.command()
    @commands.is_owner()
    @commands.check(guildcheck)
    async def isverified(self, ctx: commands.Context, discordid: int):
        with open(settings.JSON_DIR) as f:
            verified = json.load(f)
        user_id_string = str(discordid)

        if user_id_string in verified:
            await ctx.send("Verified")
        else:
            await ctx.send("Not verified")

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(owner(bot))