from discord.ext import commands

from cogs.presence.presence import update_presence


class ConfigCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def config(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is not None:
            return

        settings = self.bot.config
        await ctx.send(
            f'prefix is set to {settings.prefix}\n'
            f'deleting delay is set to {settings.delete_after:g}\n'
            f'readall limit is set to {settings.readall_limit}\n'
            f'rpc is set to {settings.custom_rpc}\n'
            f'rpc type is set to {settings.custom_rpc_type}\n'
            f'status is set to {settings.status}'
        )

    @config.command(name='prefix')
    async def config_prefix(
        self,
        ctx: commands.Context,
        prefix: str,
    ) -> None:
        self.bot.config.prefix = prefix
        self.bot.command_prefix = prefix
        await ctx.send(f'prefix set to {prefix}')

    @config.command(name='delete_after')
    async def config_delete_after(
        self,
        ctx: commands.Context,
        seconds: float,
    ) -> None:
        self.bot.config.delete_after = seconds
        await ctx.send(f'delete_after set to {seconds:g} seconds')

    @config.command(name='readall_limit')
    async def config_readall_limit(
        self,
        ctx: commands.Context,
        channels: int,
    ) -> None:
        if channels < 1:
            await ctx.send('readall_limit must be at least 1')
            return

        self.bot.config.readall_limit = channels
        await ctx.send(f'readall_limit set to {channels} channels')

    @config.command(name='rpc')
    async def config_rpc(
        self,
        ctx: commands.Context,
        *,
        text: str,
    ) -> None:
        self.bot.config.custom_rpc = text
        await update_presence(self.bot)
        await ctx.send(f'custom_rpc set to {text}')

    @config.command(name='rpc_type')
    async def config_rpc_type(
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