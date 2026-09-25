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
        super().__init__(command_prefix=config.prefix, self_bot=True)
        self.config = config

    async def get_context(self, message, /, *, cls=CleanupContext):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self) -> None:
        from cogs.cleanup import CleanupCog
        from cogs.config import ConfigCog
        from cogs.general import GeneralCog
        
        from cogs.presence import PresenceCog
        from cogs.status import StatusCog
        from cogs.rpc import RpcCog

        await self.add_cog(CleanupCog(self))
        await self.add_cog(ConfigCog(self))
        await self.add_cog(GeneralCog(self))
        await self.add_cog(PresenceCog(self))
        
        await self.add_cog(StatusCog(self))
        await self.add_cog(RpcCog(self))