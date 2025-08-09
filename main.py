import discord
from discord.ext import commands
from bot import bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("important.env")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user}")

async def main():
    async with bot:
        await bot.load_extension("cogs.economy")
        await bot.load_extension("cogs.events")
        await bot.load_extension("cogs.user_actions")
        await bot.start(os.getenv("DS_TOKEN"))

asyncio.run(main())
