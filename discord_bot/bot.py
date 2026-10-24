import discord
from discord.ext import commands
from core.config import settings
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as admin bot: {bot.user.name} ({bot.user.id})")
        await bot.load_extension("discord_bot.cogs.admin_commands")

        if __name__ == "__main__":
            asyncio.run(bot.start(settings.DISCORD_BOT_TOKEN))