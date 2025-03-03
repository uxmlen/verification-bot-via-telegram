import discord
from discord.ext import commands
import random
import string
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    filename="verification.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()


class Verification(commands.Cog):
    """Verification Cog"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Store verification codes
        self.codes = {}
        self.setup_telegram()
        logging.info("Verification bot started")

    def setup_telegram(self):
        "Setup and start Telegram bot"""
        self.tg_bot = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
        
        self.tg_bot.add_handler(CommandHandler("verify", self.telegram_verify))
        self.bot.loop.create_task(self.start_telegram())

    async def start_telegram(self):
        await self.tg_bot.initialize()
        await self.tg_bot.start()
        await self.tg_bot.run_polling()

    def make_code(self) -> str:
        """Generate 6-digit verification code"""
        return "".join(random.choices(string.digits, k=6))

    @commands.command(name="code")
    async def verify_discord(self, ctx, code: str):
        """Verify Discord user with code from Telegram"""
        user_id = ctx.author.id
        username = ctx.author.name

        if code in self.codes:
            try:
                telegram_id = self.codes[code]
                role = ctx.guild.get_role(int(os.getenv("ROLE")))
                await ctx.author.add_roles(role)

                logging.info(
                    f"Verification successful - Discord: {username}({user_id}) - "
                    f"Code: {code} - Telegram ID: {telegram_id}"
                )

                await ctx.send(
                    os.getenv("WELCOME_MESSAGE").format(user=ctx.author.mention)
                )
                del self.codes[code]

            except discord.Forbidden:
                logging.error(
                    f"Permission error - Cannot assign role to {username}({user_id})"
                )
                await ctx.send("❌ I don't have permission to assign roles!")
            except AttributeError:
                logging.error(
                    f"Role not found error - Attempted verification for {username}({user_id})"
                )
                await ctx.send("❌ Verification role not found!")
        else:
            logging.warning(
                f"Invalid code attempt - Discord: {username}({user_id}) - Code: {code}"
            )
            await ctx.send("❌ Invalid code!")

    async def telegram_verify(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate verification code in Telegram"""
        telegram_user = update.effective_user
        code = self.make_code()
        self.codes[code] = telegram_user.id

        logging.info(
            f"Code generated - Telegram: {telegram_user.username}({telegram_user.id}) - "
            f"Code: {code}"
        )

        await update.message.reply_text(
            f"Your verification code: `{code}`\n"
            f"Go to Discord and type: /code {code}"
        )


async def setup(bot):
    await bot.add_cog(Verification(bot))
