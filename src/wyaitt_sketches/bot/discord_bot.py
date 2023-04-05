import discord
import datetime
from discord.ext import commands, tasks
from wyaitt_sketches.prompt_strategy.hey_kiddo import HeyKiddoStrategy
from wyaitt_sketches.core.settings import settings

# Create a new client from the discord.py library
client = discord.Client(intents=discord.Intents.default())


# Define a coroutine to be called when the bot receives a message
@client.event
async def on_message(message):
    # Check if the message was sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message was a direct message to the bot
    if isinstance(message.channel, discord.DMChannel):
        # Check if the message contained the word "start"
        if "start" in message.content.lower():
            await send_prompt()


@tasks.loop(hours=1)
async def scheduled_message():
    # Send a message to the specified Discord group
    now = datetime.datetime.now()
    if now.hour != 19:
        return

    group = client.get_guild(settings.discord_guild_id)
    channels = group.channels
    for channel in channels:
        if channel.name == "general":

            for i in range(5):
                strategy = HeyKiddoStrategy()
                out = strategy.evaluate(datetime.date.today())
                await channel.send("\n".join([
                    out.original_title,
                    out.original_url,
                    "",
                    out.content_description,
                    "",
                    out.illustration_prompt
                ]))


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    scheduled_message.start()


async def send_prompt():
    # Send a message to the specified Discord group
    group = client.get_guild(settings.discord_guild_id)
    channels = group.channels
    for channel in channels:
        if channel.name == "general":
            await channel.send(f"{936929561302675456} /imagine prompt abc")
            break  # Only send the message to the first general channel


# Start the bot with your token (replace YOUR_TOKEN_HERE with your actual bot token)
client.run(settings.discord_bot_token)
