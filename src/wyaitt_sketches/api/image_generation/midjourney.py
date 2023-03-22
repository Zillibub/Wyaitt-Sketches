import discord
from wyaitt_sketches.core.settings import settings
import time

# Create a new client from the discord.py library
client = discord.Client()


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
            send_prompt()


def send_prompt():
    # Send a message to the specified Discord group
    group_id = 1234567890  # Replace with your group ID
    group = client.get_guild(group_id)
    channels = group.channels
    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"/imagine prompt")
            break  # Only send the message to the first text channel


# Start the bot with your token (replace YOUR_TOKEN_HERE with your actual bot token)
client.run("YOUR_TOKEN_HERE")
