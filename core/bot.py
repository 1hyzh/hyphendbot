from discord.ext import commands

from core.config import Config


class CleanupContext(commands.Context):
    async def send(self, content=None, **kwargs):
        if (
            'delete_after' not in kwargs
            and self.bot.config.delete_after > 0
        ):
            kwargs['delete_after'] = self.bot.config.delete_after
        return await super().send(content, **kwargs)


class HyphendBot(commands.Bot):
    def __init__(self, config: Config) -> None:
        super().__init__(
            command_prefix=config.prefix,
            self_bot=True,
            help_command=None,
        )
        self.config = config
        self.add_check(self._only_running_account)

    async def _only_running_account(self, ctx: commands.Context) -> bool:
        return self.user is not None and ctx.author.id == self.user.id

    async def get_context(self, message, /, *, cls=CleanupContext):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self) -> None:
        from cogs.coreutils.cleanup import CleanupCog
        from cogs.coreutils.config import ConfigCog
        from cogs.general import GeneralCog
        from cogs.presence.presence import PresenceCog
        from cogs.presence.status import StatusCog
        from cogs.presence.rpc import RpcCog
        from cogs.people.block import BlockCog
        from cogs.stupidthings.ngh import NghmodeCog
        from cogs.utils.readall import ReadAllCog
        
        
        await self.add_cog(CleanupCog(self))
        await self.add_cog(ConfigCog(self))
        await self.add_cog(GeneralCog(self))
        await self.add_cog(PresenceCog(self))
        await self.add_cog(StatusCog(self))
        await self.add_cog(RpcCog(self))
        await self.add_cog(BlockCog(self))
        await self.add_cog(NghmodeCog(self))
        await self.add_cog(ReadAllCog(self))
        