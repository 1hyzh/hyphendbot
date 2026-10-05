from cogs.presence.presence import update_presence
from discord.ext import commands


class RpcCog(commands.Cog): # main class
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def rpc(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send('use `>rpc text <text>` or `>rpc type <type>`')

    @rpc.command(name='text')
    async def rpc_text(
        self,
        ctx: commands.Context, # context :-:
        *,
        text: str,
    ) -> None:
        self.bot.config.custom_rpc = text # sets your rpc to the text inputted 
        await update_presence(self.bot)
        await ctx.send(f'rpc text set to `{text}`') # output when the presence has been updated

    @rpc.command(name='type')
    async def rpc_type(
        self,
        ctx: commands.Context, # context :-: again
        activity_type: str,
    ) -> None:
        activity_type = activity_type.lower() # i dont want u screamin at me
        if activity_type not in {'playing', 'listening', 'streaming'}: # rpc types
            await ctx.send('use `playing`, `listening`, or `streaming`')
            return

        self.bot.config.custom_rpc_type = activity_type # sets rpc activity type
        await update_presence(self.bot) 
        await ctx.send(f'rpc type set to `{activity_type}`') # output when the presence has been updated