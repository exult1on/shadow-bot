from discord.ext import commands

class exts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
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
    async def unload(self, ctx, command: str):
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