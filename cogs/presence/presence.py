import discord
from discord.ext import commands

STATUS_VALUES = {
    'online': discord.Status.online,
    'idle': discord.Status.idle,
    'dnd': discord.Status.dnd,
    'invisible': discord.Status.invisible,
}


def build_custom_activity(config) -> discord.Activity:
    activity_type = config.custom_rpc_type
    if activity_type == 'listening':
        return discord.Activity(
            type=discord.ActivityType.listening,
            name=config.custom_rpc,
        )
    if activity_type == 'streaming':
        return discord.Streaming(
            name=config.custom_rpc,
            url=config.custom_rpc_url or 'https://twitch.tv/',
        )
    return discord.Game(name=config.custom_rpc)


def build_status(config) -> discord.Status:
    return STATUS_VALUES.get(config.status, discord.Status.online)


async def update_presence(bot: commands.Bot) -> None:
    await bot.change_presence(
        activity=build_custom_activity(bot.config),
        status=build_status(bot.config),
    )


class PresenceCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await update_presence(self.bot)