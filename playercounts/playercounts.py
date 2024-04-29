import settings
import datetime
import importlib
from settings import roblox
from roblox.jobs import ServerType
from openpyxl import load_workbook
from discord.ext import commands, tasks

utc = datetime.timezone.utc

times = [
    datetime.time(hour=0, tzinfo=utc),
    datetime.time(hour=3, tzinfo=utc),
    datetime.time(hour=6, tzinfo=utc),
    datetime.time(hour=9, tzinfo=utc),
    datetime.time(hour=12, tzinfo=utc),
    datetime.time(hour=15, tzinfo=utc),
    datetime.time(hour=18, tzinfo=utc),
    datetime.time(hour=21, tzinfo=utc)
]

class plrc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(time=times)
    async def islandcounts(self):
        for xlsx_file in settings.XLSX_DIR.glob('*.xlsx'):
            if xlsx_file.name == 'rupert.xlsx':
                islandId = 5465507265
            elif xlsx_file.name == 'canter.xlsx':
                islandId = 5620237741
            elif xlsx_file.name == 'stonemore.xlsx':
                islandId = 6249721735
            elif xlsx_file.name == 'ellesmere.xlsx':
                islandId = 5620227713
            else:
                islandId = 5620237900

            wb = load_workbook(xlsx_file)
            ws = wb.active

            place = roblox.get_base_place(islandId)

            playing_island = 0
            async for server in place.get_servers(server_type=ServerType.public, page_size=25):
                    playing_island += server.playing
            dt_string = datetime.datetime.now(utc).strftime("%d/%m/%y %H:%M")

            new_data = [[dt_string, playing_island]]
            for row in new_data:
                ws.append(row)

            wb.save(xlsx_file)

async def setup(bot):
    importlib.reload(settings)
    plrc.islandcounts.start()
    await bot.add_cog(plrc(bot))