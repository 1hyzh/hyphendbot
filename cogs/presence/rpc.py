from cogs.presence.presence import update_presence
from discord.ext import commands


class RpcCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def rpc(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send('use >rpc text <text> or >rpc type <type>')

    @rpc.command(name='text')
    async def rpc_text(
        self,
        ctx: commands.Context,
        *,
        text: str,
    ) -> None:
        self.bot.config.custom_rpc = text
        await update_presence(self.bot)
        await ctx.send(f'rpc text set to {text}')

    @rpc.command(name='type')
    async def rpc_type(
        self,
        ctx: commands.Context,
        activity_type: str,
    ) -> None:
        activity_type = activity_type.lower()
        if activity_type not in {'playing', 'listening', 'streaming'}:
            await ctx.send('use playing, listening, or streaming')
            return

        self.bot.config.custom_rpc_type = activity_type
        await update_presence(self.bot)
        await ctx.send(f'rpc type set to {activity_type}')