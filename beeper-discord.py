import discord
from discord.ext import commands, tasks
import aiohttp
import json

TOKEN = 'your-discord-bot-token'
CHANNEL_ID = 123456789
API_URL_1 = 'https://beeperstatus.com/summary.json'
API_URL_2 = 'https://beeperstatus.com/v2/components.json'
API_URL_3 = 'https://updates.beeper.com/updates.json'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    check_api.start()  # Start the task when the bot is ready
    check_updates.start()  # Start the updates check when the bot is ready

@tasks.loop(minutes=1)  # Check every 1 minute
async def check_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_1) as response1:
            data1 = await response1.json()
            if data1['page']['status'] != 'UP':
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(f'There is an outage! Status: {data1["page"]["status"]}')

        async with session.get(API_URL_2) as response2:
            data2 = await response2.json()
            for component in data2:
                if component['status'] != 'OPERATIONAL':
                    channel = bot.get_channel(CHANNEL_ID)
                    await channel.send(f'Component {component["name"]} is not operational! Status: {component["status"]}')

@tasks.loop(minutes=1)  # Check every 1 minute
async def check_updates():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_3) as response3:
            data3 = await response3.json()
            for item in data3['items']:
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(f'Update: {item["content_text"]}')

bot.run(TOKEN)