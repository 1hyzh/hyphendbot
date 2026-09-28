import asyncio
import io
from typing import Any, Dict, Optional

import aiohttp
import discord
from discord.ext import commands, tasks
from pypresence import ActivityType, Presence
from pypresence.exceptions import PyPresenceException

from cogs.lastfm.imagehandler import (
    get_album_image,
    get_album_name,
    get_full_quality_image,
    get_rpc_image,
)
from cogs.presence.presence import update_presence


LASTFM_ENDPOINT = 'https://ws.audioscrobbler.com/2.0/'


class DesktopRpc:
    def __init__(self, application_id: str) -> None:
        self.application_id = application_id
        self.client: Optional[Presence] = None

    async def update(self, track: Dict[str, Any], fallback_image_key: Optional[str] = None) -> None:
        await asyncio.to_thread(self._update, track, fallback_image_key)

    def _update(self, track: Dict[str, Any], fallback_image_key: Optional[str] = None) -> None:
        try:
            if self.client is None:
                self.client = Presence(self.application_id)
                self.client.connect()

            artist = track['artist']['#text'].strip()
            album = get_album_name(track)
            image_url = get_rpc_image(track)
            large_image = image_url or fallback_image_key or None

            self.client.update(
                activity_type=ActivityType.LISTENING,
                name='music',
                details=track['name'].strip(),
                state=album or artist,
                large_image=large_image,
                large_text=artist if (artist and album) else (album or artist),
                large_url=image_url or None,
            )
        except Exception:
            self.client = None
            raise

    async def clear(self) -> None:
        if self.client is not None:
            try:
                await asyncio.to_thread(self.client.clear)
            except Exception:
                self.client = None

    async def close(self) -> None:
        if self.client is not None:
            try:
                await asyncio.to_thread(self.client.close)
            except Exception:
                pass
            finally:
                self.client = None


class LastFmRpcCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_track_key: Optional[str] = None
        self.desktop_rpc: Optional[DesktopRpc] = None
        self._asset_cache: Dict[str, str] = {}
        if bot.config.lastfm_application_id:
            self.desktop_rpc = DesktopRpc(bot.config.lastfm_application_id)
        self.lastfm_rpc.start()

    def cog_unload(self) -> None:
        self.lastfm_rpc.cancel()
        if self.session is not None and not self.session.closed:
            self.bot.loop.create_task(self.session.close())
        if self.desktop_rpc is not None:
            self.bot.loop.create_task(self.desktop_rpc.close())

    @tasks.loop(seconds=60)
    async def lastfm_rpc(self) -> None:
        config = self.bot.config
        if not config.lastfm_api_key or not config.lastfm_username:
            return

        await self.ensure_session()

        try:
            track = await self.fetch_current_track()
        except (aiohttp.ClientError, KeyError, TypeError, ValueError):
            return

        if track is None:
            if self.last_track_key is not None:
                self.last_track_key = None
                await update_presence(self.bot)
                await self.clear_desktop_rpc()
            return

        track_key = ':'.join((track['artist']['#text'], track['name']))
        if track_key == self.last_track_key:
            return

        self.last_track_key = track_key
        activity = await self.build_activity(track)
        await update_presence(self.bot, activity)
        await self.update_desktop_rpc(track)

    @lastfm_rpc.before_loop
    async def before_lastfm_rpc(self) -> None:
        await self.bot.wait_until_ready()
        self.lastfm_rpc.change_interval(
            seconds=self.bot.config.lastfm_poll_interval,
        )

    async def fetch_current_track(self) -> Optional[Dict[str, Any]]:
        await self.ensure_session()
        params = {
            'method': 'user.getrecenttracks',
            'user': self.bot.config.lastfm_username,
            'api_key': self.bot.config.lastfm_api_key,
            'format': 'json',
            'limit': '1',
            'autocorrect': '1',
        }
        async with self.session.get(
            LASTFM_ENDPOINT,
            params=params,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as response:
            response.raise_for_status()
            payload = await response.json()

        tracks = payload.get('recenttracks', {}).get('track', [])
        if not tracks:
            return None

        track = tracks[0]
        nowplaying = str(track.get('@attr', {}).get('nowplaying', '')).lower()
        if nowplaying not in {'1', 'true'}:
            return None
        return track

    async def ensure_session(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def update_desktop_rpc(self, track: Dict[str, Any]) -> None:
        if self.desktop_rpc is None:
            return
        try:
            await self.desktop_rpc.update(track, fallback_image_key=self.bot.config.lastfm_image_key)
        except (ConnectionError, OSError, RuntimeError, PyPresenceException):
            self.desktop_rpc.client = None

    async def clear_desktop_rpc(self) -> None:
        if self.desktop_rpc is None:
            return
        try:
            await self.desktop_rpc.clear()
        except (ConnectionError, OSError, RuntimeError, PyPresenceException):
            self.desktop_rpc.client = None

    async def build_activity(self, track: Dict[str, Any]) -> discord.Activity:
        config = self.bot.config
        artist = track['artist']['#text'].strip()
        title = track['name'].strip()
        album = get_album_name(track)
        image_url = get_rpc_image(track)

        large_image = None
        if image_url and config.lastfm_application_id:
            try:
                app_id = int(config.lastfm_application_id)
                if image_url in self._asset_cache:
                    large_image = self._asset_cache[image_url]
                else:
                    proxied = await self.bot.proxy_external_application_assets(app_id, image_url)
                    if proxied:
                        large_image = proxied[0]
                        self._asset_cache[image_url] = large_image
            except Exception:
                pass

        if not large_image:
            if config.lastfm_image_key:
                large_image = config.lastfm_image_key
            elif image_url:
                large_image = image_url

        assets = None
        if large_image:
            large_text = artist if (artist and album) else (album or artist)
            assets = discord.ActivityAssets(
                large_image=large_image,
                large_text=large_text or None,
            )

        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name='music',
            details=title,
            state=album or artist,
            assets=assets,
        )
        if config.lastfm_application_id:
            activity.application_id = int(config.lastfm_application_id)
        return activity

    @commands.command(name='lastfm')
    async def lastfm_status(self, ctx: commands.Context) -> None:
        config = self.bot.config
        if not config.lastfm_api_key or not config.lastfm_username:
            await ctx.send('Last.fm is not configured.')
            return
        try:
            track = await self.fetch_current_track()
        except (aiohttp.ClientError, KeyError, TypeError, ValueError):
            await ctx.send('Last.fm could not be reached right now.')
            return
        if track is None:
            await ctx.send(f'No track is currently playing for `{config.lastfm_username}`.')
            return
        self.last_track_key = ':'.join((track['artist']['#text'], track['name']))
        activity = await self.build_activity(track)
        await update_presence(self.bot, activity)
        await self.update_desktop_rpc(track)
        await ctx.send(
            f"listening to `{track['name']}` by `{track['artist']['#text']}`"
        )

    @commands.command(name='cover')
    async def cover(self, ctx: commands.Context) -> None:
        config = self.bot.config
        if not config.lastfm_api_key or not config.lastfm_username:
            await ctx.send('Last.fm is not configured.')
            return
        try:
            track = await self.fetch_current_track()
        except (aiohttp.ClientError, KeyError, TypeError, ValueError):
            await ctx.send('Last.fm could not be reached right now.')
            return
        if track is None:
            await ctx.send(f'No track is currently playing for `{config.lastfm_username}`.')
            return

        image_url = get_full_quality_image(track)
        if not image_url:
            await ctx.send('Last.fm did not provide cover art for the current track.')
            return

        await self.ensure_session()
        try:
            async with self.session.get(
                image_url,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                response.raise_for_status()
                image_data = await response.read()
        except (aiohttp.ClientError, ValueError):
            await ctx.send(image_url)
            return

        artist = track['artist']['#text'].strip()
        album = get_album_name(track)
        caption = f"{track['name'].strip()} by {artist}"
        if album:
            caption += f" - {album}"
        await ctx.send(
            caption,
            file=discord.File(io.BytesIO(image_data), filename='cover.jpg'),
        )
