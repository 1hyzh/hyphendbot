import asyncio

import discord
from discord.ext import commands


class CleanupCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        is_command_message = message.content.startswith(self.bot.config.prefix)

        if is_command_message:
            self.schedule(message)

    def schedule(self, message: discord.Message) -> None:
        asyncio.create_task(self._delete_later(message))

    async def _delete_later(self, message: discord.Message) -> None:
        if self.bot.config.delete_after <= 0:
            return

        await asyncio.sleep(self.bot.config.delete_after)
        try:
            await message.delete()
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass