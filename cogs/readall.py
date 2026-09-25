import asyncio

import discord
from discord.ext import commands


class ReadAllCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def readall(
        self,
        ctx: commands.Context,
        scope: str = 'all',
    ) -> None:
        scope = scope.lower()
        if scope not in {'all', 'servers', 'dms'}:
            await ctx.send('usage: >readall all|servers|dms')
            return

        await ctx.send(f'started reading {scope}')
        channels = self._channels_for(scope)
        read_count = 0
        failed_count = 0
        limited = False

        for channel_number, channel in enumerate(channels, start=1):
            if (
                scope in {'all', 'servers'}
                and channel_number > self.bot.config.readall_limit
            ):
                limited = True
                break

            try:
                await channel.ack()
                read_count += 1
            except (
                AttributeError,
                discord.Forbidden,
                discord.HTTPException,
                discord.NotFound,
            ):
                failed_count += 1
            except Exception:
                failed_count += 1

            if self.bot.config.readall_delay > 0:
                await asyncio.sleep(self.bot.config.readall_delay)

        result = f'read {read_count} {scope} channel(s)'
        if failed_count:
            result += f'; {failed_count} failed'
        if limited:
            result += f'; limit {self.bot.config.readall_limit} reached'
        await ctx.send(result)

    def _channels_for(self, scope: str):
        if scope in {'all', 'servers'}:
            for guild in self.bot.guilds:
                seen = set()
                for channel in (*guild.channels, *guild.threads):
                    if not isinstance(
                        channel,
                        (discord.TextChannel, discord.Thread),
                    ):
                        continue
                    if channel.id in seen:
                        continue
                    seen.add(channel.id)
                    yield channel

        if scope in {'all', 'dms'}:
            for channel in self.bot.private_channels:
                if isinstance(
                    channel,
                    (discord.DMChannel, discord.GroupChannel),
                ):
                    yield channel