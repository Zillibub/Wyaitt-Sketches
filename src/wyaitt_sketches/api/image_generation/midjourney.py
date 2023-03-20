import discord
from wyaitt_sketches.core.settings import settings


class MidJourneyAPI:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.default())

    async def print_guilds(self):
        """
        Printing all servers this bot has access to
        :return:
        """
        await self.client.login(settings.discord_bot_token)
        for guild in self.client.guilds:
            print(f"- {guild.id} (name: {guild.name})")

    async def send_message(self, bot_id, message):
        # log in to Discord with the bot token
        await self.client.login(settings.discord_bot_token)

        # get the user object of the bot
        bot_user = await self.client.fetch_user(bot_id)

        # send a direct message to the bot
        await bot_user.send(message)
