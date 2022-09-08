import asyncio
import os

import discord
from discord.ext import commands

from help import JapaneseHelpCommand


PREFIX = "/"
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


async def main():
    help_command = JapaneseHelpCommand(prefix=PREFIX)
    intents = discord.Intents.all()
    bot = commands.Bot(
        command_prefix=PREFIX,
        help_command=help_command,
        intents=intents)
    cog = "judge"

    await bot.load_extension(cog)
    await bot.start(token=TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
