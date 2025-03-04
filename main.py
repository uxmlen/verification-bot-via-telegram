"""This is the main file for the bot."""

import discord
import os
import sys
import asyncio
import logging
from discord.ext import commands
from discord.utils import get
from pathlib import Path
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        logging.info("Bot initialization started")

    async def on_ready(self):
        logging.info(f"Bot is ready and logged in as {self.user}")
        logging.info("=== Configuration ===")
        logging.info(f"Discord Bot ID: {self.user.id}")
        logging.info(f"Role ID: {os.getenv('ROLE')}")
        logging.info(f"Channel ID: {os.getenv('CHANNEL')}")

        activity_name = ".verify"
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=activity_name,
            )
        )

    async def setup_hook(self):
        """Load all cogs"""
        logging.info("Starting to load cogs...")
        cog_path = Path("./cogs")

        for file in cog_path.glob("*.py"):
            try:
                await self.load_extension(f"cogs.{file.stem}")
                logging.info(f"Successfully loaded cog: {file.stem}")
            except Exception as e:
                logging.error(f"Failed to load cog {file.stem}: {e}")

        logging.info("Finished loading cogs")


async def main() -> None:
    """Main entry point for the bot"""
    bot = Bot()
    logging.info("Starting bot...")
    await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    load_dotenv()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot shutdown initiated by user")
    except Exception as e:
        logging.critical(f"Unexpected error: {str(e)}")
        raise e
