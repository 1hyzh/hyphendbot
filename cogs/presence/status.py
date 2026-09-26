from discord.ext import commands

from cogs.presence.presence import STATUS_VALUES, update_presence


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def status(
        self,
        ctx: commands.Context,
        *,
        value: str = '',
    ) -> None:
        if ctx.invoked_subcommand is not None:
            return

        value = value.strip().lower()
        if value not in STATUS_VALUES:
            await ctx.send('use online, idle, dnd, or invisible')
            return

        self.bot.config.status = value
        await update_presence(self.bot)
        await ctx.send(f'status set to {value}')

    