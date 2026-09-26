from discord.ext import commands

from core.config import Config


def style_response(content):
    if not isinstance(content, str):
        return content

    return '\n'.join(
        line
        if not line.strip() or line.startswith(('- ', '# hyphend bot'))
        else f'- {line}'
        for line in content.splitlines()
    )


class CleanupContext(commands.Context):
    async def send(self, content=None, **kwargs):
        content = style_response(content)
        if (
            'delete_after' not in kwargs
            and self.bot.config.delete_after > 0
        ):
            kwargs['delete_after'] = self.bot.config.delete_after
        return await super().send(content, **kwargs)


class HyphendHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping) -> None:
        commands_list = []
        for command in sorted(self.context.bot.commands, key=lambda item: item.name):
            if command.hidden:
                continue

            usage = command.name
            if command.signature:
                usage += f' {command.signature}'
            commands_list.append(usage)

        prefix = self.context.bot.config.prefix
        command_lines = '\n'.join(f'{prefix}{command}' for command in commands_list)
        await self.context.send(
            f'# hyphend bot '
            f'version: {self.context.bot.config.wt}\n'
            f'commands:\n{command_lines}'
        )

    async def send_command_help(self, command) -> None:
        prefix = self.context.bot.config.prefix
        usage = f'{prefix}{command.qualified_name}'
        if command.signature:
            usage += f' {command.signature}'
        description = command.help or 'no description available'
        await self.context.send(
            f'# hyphend bot '
            f'version: {self.context.bot.config.wt}\n'
            f'command: {usage}\n'
            f'info: {description}'
        )


class HyphendBot(commands.Bot):
    def __init__(self, config: Config) -> None:
        super().__init__(
            command_prefix=config.prefix,
            self_bot=True,
            help_command=HyphendHelpCommand(),
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
        