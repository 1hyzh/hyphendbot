from discord.ext import commands


class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send('pong!')

    @commands.command()
    async def health(self, ctx: commands.Context) -> None:
        latency = self.bot.latency
        if latency == float('inf'):
            latency_text = 'unavailable'
        else:
            latency_text = f'{latency * 1000:.0f} ms'

        await ctx.send(
            f'# hyphend bot\n'
            f'version: {self.bot.config.wt}\n'
            f'health: online\n'
            f'latency: {latency_text}'
        )