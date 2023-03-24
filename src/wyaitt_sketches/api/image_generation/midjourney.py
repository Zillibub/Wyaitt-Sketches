import discord
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
