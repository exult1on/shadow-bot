import os
import pathlib
from roblox import Client
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DiscordToken")
ROBLOX_TOKEN = os.getenv("RobloxToken")

BASE_DIR = pathlib.Path(__file__).parent

CMD_DIR = BASE_DIR / "commands"
COG_DIR = BASE_DIR / "cogs"
JSON_DIR = BASE_DIR / "verified.json"

# Server IDs
ServerID = 740209431387701428
Logs_Channel = 1220779980938543174
ServerMSG_Channel = 740220101428772864

# Role IDs
role_verified = 933285009102622800
role_unverified = 933396416305455135

# Roblox
roblox = Client(ROBLOX_TOKEN)
GroupID = 8341068

# Colours
BootEmbed = 0x234633

# Command IDs
VerifyCommandID = 000