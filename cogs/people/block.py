import discord
from discord.ext import commands

from core.targets import resolve_user


class BlockCog(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@commands.command()
	async def block(
		self,
		ctx: commands.Context,
		*,
		target: str = '',
	) -> None:
		target = target.strip()
		if not target:
			target = ''

		try:
			user = await resolve_user(ctx, target)
		except commands.BadArgument:
			await ctx.send('usage: >block @username or reply to a user')
			return

		if self.bot.user is not None and user.id == self.bot.user.id:
			await ctx.send('you cannot block the account running this bot')
			return

		try:
			await user.block()
		except (discord.Forbidden, discord.HTTPException):
			await ctx.send(f'could not block {user}')
			return

		await ctx.send(f'blocked {user}')

	@commands.command()
	async def unblock(
		self,
		ctx: commands.Context,
		*,
		target: str = '',
	) -> None:
		target = target.strip()
		if not target:
			target = ''

		try:
			user = await resolve_user(ctx, target)
		except commands.BadArgument:
			await ctx.send('usage: >unblock @username or reply to a user')
			return

		if self.bot.user is not None and user.id == self.bot.user.id:
			await ctx.send('you cannot unblock the account running this bot')
			return

		try:
			await user.unblock()
		except (discord.Forbidden, discord.HTTPException):
			await ctx.send(f'could not unblock {user}')
			return

		await ctx.send(f'unblocked {user}')