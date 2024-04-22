import discord
import settings
import datetime
import importlib
from settings import roblox
from discord import app_commands
from discord.ext import commands
from roblox.jobs import ServerType 

class islands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "islands", description = "Get information about the current amount of players on NORTHWIND islands")
    @app_commands.guilds(settings.ServerID)
    @app_commands.describe(island="Islands to choose from")
    @app_commands.choices(island=[
        discord.app_commands.Choice(name="Rupert", value=1),
        discord.app_commands.Choice(name="Cantermagne", value=2),
        discord.app_commands.Choice(name="Stonemore", value=3),
        discord.app_commands.Choice(name="Ellesmere", value=4),
        discord.app_commands.Choice(name="Beauval", value=5)
        ])
    async def islands(self, interaction: discord.Interaction, island: discord.app_commands.Choice[int]):
        logs_channel = self.bot.get_channel(settings.Logs_Channel)
        if island.value == 1:
            islandId = 5465507265
        elif island.value == 2:
            islandId = 5620237741
        elif island.value == 3:
            islandId = 6249721735
        elif island.value == 4:
            islandId = 5620227713
        else:
            islandId = 5620237900

        place = roblox.get_base_place(islandId)

        embed = discord.Embed(
            title=islands.name,
            url="https://www.roblox.com/games/{0}" .format(islandId),
            timestamp=datetime.datetime.now(),
            color=0x002C3C)
        embed.set_image(url="https://tr.rbxcdn.com/28763fc1173b166b4f3bc9d2e2796f9e/768/432/Image/Png")

        playing_island = 0
        servers_island = 0
        async for server in place.get_servers(server_type=ServerType.public, page_size=25):
            playing_island += server.playing
            servers_island += 1
            embed.add_field(
                name="Server {0}" .format(servers_island),
                value="Player count: {0}\nPing (Europe): {1}\nAverage FPS: {2}" .format(server.playing, server.ping, round(server.fps, 1)),
                inline=True)

        embed.description = "Total player count: {0}\nAmount of servers: {1}" .format(playing_island, servers_island)

        embed.set_footer(
            text="Requested by {0}" .format(interaction.user.name),
            icon_url=interaction.user.avatar)

        if servers_island == 25:
            user = await self.bot.fetch_user(836977956261330944)
            await user.send("{0} reached {1} servers, you should probably increase the api request"
                        .format(islands.name, len(servers_island)))

        if interaction.channel.id == settings.Bot_Channel:
            await interaction.response.send_message(content="There are currently {0} players active on {1}" .format(playing_island, islands.name), embed=embed)
        else:
            await interaction.response.send_message(content="There are currently {0} players active on {1}" .format(playing_island, islands.name), embed=embed, ephemeral=True)
        await logs_channel.send("**{0}** used the 'islands' command"
            .format(interaction.user.name))

async def setup(bot):
    importlib.reload(settings)
    await bot.add_cog(islands(bot))