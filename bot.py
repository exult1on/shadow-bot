import discord
import settings
from os import path
from discord.ext import commands
from typing import Literal, Optional

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

if path.isfile(settings.JSON_DIR) is False:
    raise Exception("\n\nFile not found\n")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.event
async def on_ready():

    # Loading cogs on boot
    for cog_file in settings.COG_DIR.glob("*.py"):
        if cog_file.name != "__init__.py":
            await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
            print(f"{cog_file.name} loaded")

    # Loading commands on boot
    for cmd_file in settings.CMD_DIR.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.load_extension(f"commands.{cmd_file.name[:-3]}")
            print(f"{cmd_file.name} loaded")

bot.run(settings.DISCORD_TOKEN)