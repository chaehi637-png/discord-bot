import discord
from discord.ext import commands
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

TOKEN = "봇토큰"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds, scope
)

client_sheet = gspread.authorize(creds)
sheet = client_sheet.open("근무기록").sheet1

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

join_times = {}

@bot.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and after.channel is not None:
        join_times[member.id] = datetime.now()

    elif before.channel is not None and after.channel is None:

        if member.id in join_times:

            join_time = join_times[member.id]
            leave_time = datetime.now()

            duration = leave_time - join_time

            sheet.append_row([
                member.name,
                str(join_time),
                str(leave_time),
                str(duration)
            ])

            del join_times[member.id]

            print(f"{member.name} 저장 완료")

bot.run(TOKEN)
