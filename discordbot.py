import asyncio
import os

import discord
from discord.ext import commands


async def main():
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
    token = os.getenv('DISCORD_BOT_TOKEN')
    await bot.load_extension('judge')
    await bot.start(token=token)


if __name__ == '__main__':
    asyncio.run(main())
