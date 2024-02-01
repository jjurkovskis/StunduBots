import discord
from discord.ext import commands
from icalendar import Calendar
from datetime import datetime, timedelta
import pytz

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def get_lectures_on_date(filename, target_date):
    with open(filename, 'rb') as file:
        calendar = Calendar.from_ical(file.read())

    lectures_on_date = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt

            if isinstance(dtstart, datetime) and dtstart.date() == target_date:
                start_time = dtstart.strftime("%H:%M")
                end_time = dtend.strftime("%H:%M")
                summary = str(component.get('summary'))
                lectures_on_date.append(f"{summary} from {start_time} to {end_time}")

    return lectures_on_date

@bot.command(name='today')
async def today(ctx):
    today_date = datetime.now().date()
    lectures = get_lectures_on_date('Studenta_grafiks_23_24-P.ics', today_date)
    if lectures:
        response = '\n'.join(lectures)
    else:
        response = "No lectures scheduled for today."
    await ctx.send(response)

@bot.command(name='tomorrow')
async def tomorrow(ctx):
    tomorrow_date = datetime.now().date() + timedelta(days=1)
    lectures = get_lectures_on_date('Studenta_grafiks_23_24-P.ics', tomorrow_date)
    if lectures:
        response = '\n'.join(lectures)
    else:
        response = "No lectures scheduled for tomorrow."
    await ctx.send(response)
bot.run('MTIwMjM5NTk5MTUwMDY1MjU2NA.G5cCNV.MIv9bmr1Es9mcwWzDKOWy6KqBcsUKNYJ8XikyE')

