import asyncio

import discord
from discord.ext import commands


class NghmodeCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.enabled = False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if (
            not self.enabled
            or self.bot.user is None
            or message.author.id != self.bot.user.id
            or message.content.startswith(self.bot.config.prefix)
        ):
            return

        await asyncio.sleep(1)
        if not self.enabled:
            return

        try:
            await message.edit(content=f'{message.content} nghhh')
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

    @commands.command(name='ngh', aliases=['nghmode'])
    async def nghmode(
        self,
        ctx: commands.Context,
        value: str,
    ) -> None:
        value = value.lower()
        if value not in {'true', 'false'}:
            await ctx.send('usage: >ngh true|false')
            return

        self.enabled = value == 'true'
        await ctx.send(f'ngh mode {"enabled" if self.enabled else "disabled"}')