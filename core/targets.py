import discord
from discord.ext import commands


async def resolve_user(ctx: commands.Context, target: str = '') -> discord.User:
    target = target.strip()
    if target:
        if target.startswith('@') and not target.startswith('<@'):
            target = target[1:]
        return await commands.UserConverter().convert(ctx, target)

    reference = ctx.message.reference
    if reference is not None:
        resolved = reference.resolved
        if isinstance(resolved, discord.Message):
            return resolved.author

        if reference.message_id is not None:
            try:
                message = await ctx.channel.fetch_message(reference.message_id)
                return message.author
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass

    raise commands.BadArgument('mention a user or reply to their message')