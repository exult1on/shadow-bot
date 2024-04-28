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
PLRC_DIR = BASE_DIR / "playercounts"
JSON_DIR = BASE_DIR / "verified.json"

# Server IDs
ServerID = 740209431387701428
Bot_Channel = 884059197258485840
Logs_Channel = 1220779980938543174
Verify_Channel = 933290198094196767
Welcome_Channel = 841770111391629392
ServerMSG_Channel = 740220101428772864

# Role IDs
role_admin = 776464568901304370
role_ranked = 740209774016331807
role_verified = 933285009102622800
role_unverified = 933396416305455135

# Role list
AcceptRoles = [
    740209774016331807,  # Shadow
    1193194473459548320  # Bandit
]

# Roblox
roblox = Client(ROBLOX_TOKEN)
GroupID = 8341068

# Emoji IDs
AcceptEmoji = 928733132771950642

# Colours
BootEmbed = 0x234633

# Command IDs
VerifyCommandID = 1223685053146468415
ReverifyCommandID = 1229709123394867201