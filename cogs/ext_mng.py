import settings
from discord.ext import commands

def guildcheck(ctx):
    return ctx.guild.id == settings.ServerID

class exts(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    @commands.check(guildcheck)
    async def load(self, ctx, type: str, command: str):
        if type == "cog":
            type = "cogs"
        elif type == "command":
            type = "commands"
        else:
            await ctx.send(f"Unexpected type")

        try:
            await self.bot.load_extension(f"{type}.{command}")
            await ctx.send(f"The {command} {type} has been loaded")
            print(f"{command}.py loaded")

        except commands.ExtensionNotFound:
            await ctx.send(f"Command not found")

        except commands.ExtensionAlreadyLoaded:
            await self.bot.reload_extension(f"{type}.{command}")
            await ctx.send(f"The {command} {type} already loaded, reloading")
            print(f"{command}.py reloaded")
        
    @commands.command()
    @commands.is_owner()
    @commands.check(guildcheck)
    async def unload(self, ctx, type: str, command: str):
        if command == "ext_mng":
            await ctx.send(f"Can't unload the extension manager or the bot will be softlocked, try reloading")
        else:
            if type == "cog":
                type = "cogs"
            elif type == "command":
                type = "commands"
            else:
                await ctx.send(f"Unexpected type")

            try:
                await self.bot.unload_extension(f"{type}.{command}")
                await ctx.send(f"The {command} {type} has been unloaded")
                print(f"{command}.py unloaded")

            except commands.ExtensionNotLoaded:
                await ctx.send(f"The {command} {type} is not loaded")
        
async def setup(bot):
    await bot.add_cog(exts(bot))