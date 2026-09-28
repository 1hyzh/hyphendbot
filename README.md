# hyphendbot

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Coolify

Deploy this repository as a Dockerfile-based worker. Coolify will use the included `Dockerfile`; no public port is required because this is a Discord gateway process.

Add these environment variables in Coolify:

```env
TOKEN=your-discord-token
PREFIX=>
DELETE_AFTER=10
READALL_DELAY=2
READALL_LIMIT=25
CUSTOM_RPC=hyphendbot
CUSTOM_RPC_TYPE=playing
CUSTOM_RPC_URL=
STATUS=online
LASTFM_API_KEY=your-lastfm-api-key
LASTFM_USERNAME=your-lastfm-username
LASTFM_POLL_INTERVAL=60
LASTFM_APPLICATION_ID=
LASTFM_IMAGE_KEY=
```

The local `env` file is excluded from the image. Keep the token in Coolify's environment settings and enable automatic restart so the worker starts again after a crash or redeploy.

The bot reads configuration from the `env` file:

```env
token=your-discord-token
prefix=>
delete_after=10
custom_rpc=hyphendbot
custom_rpc_type=playing
custom_rpc_url=
status=online
readall_delay=2
readall_limit=25
lastfm_api_key=your-lastfm-api-key
lastfm_username=your-lastfm-username
lastfm_poll_interval=60
lastfm_application_id=
lastfm_image_key=
```

`delete_after` controls how long prefix command messages and explicitly scheduled command responses remain visible. Set it to `0` or a negative value to disable deletion.

Runtime configuration commands:

```text
>config
>config prefix !
>config delete_after 5
>config readall_limit 25
>config rpc Listening to music
>config rpc_type listening
>rpc text Listening to music
>rpc type listening
>status dnd
>lastfm
>cover
>friend @username
>block @username
>unblock @username
>readall all
>readall servers
>readall dms
```

`>friend`, `>block`, and `>unblock` accept a Discord mention or username. They also target the author of the message being replied to when no target is provided.
`readall_delay` controls the pause between channel acknowledgements. The command acknowledges all supported server channels, active threads, and private channels; it does not download their full message history.
`readall_limit` caps `>readall all` and `>readall servers` per run.

Every response sent through a command context, including help output, uses the configured deletion delay.

## Last.fm RPC

Create a Last.fm API application and put its API key in `LASTFM_API_KEY`. Set `LASTFM_USERNAME` to the account whose current scrobble should appear in the presence. The public `user.getrecenttracks` endpoint does not require the Last.fm shared secret or a user session.

When `LASTFM_APPLICATION_ID` is set, album artwork is dynamically resolved and displayed in both the Discord Gateway presence (proxied via Discord's application asset proxy) and local Discord Desktop IPC (via Rich Presence). `LASTFM_IMAGE_KEY` is supported as an optional fallback application asset key.

Discord IPC requires the Discord desktop client to be running locally; it will not work from the Docker/Coolify deployment. The `>cover` command works in both setups and sends the current dynamic artwork directly.

The cog polls every 60 seconds by default, only replaces the manual RPC while a track is marked as currently playing, and restores the configured manual RPC when playback stops. The RPC displays `Listening to music`, followed by the track title, album, and artist. Use `>lastfm` to check the configured account and immediately set the RPC to its current track. Use `>cover` to send the current album artwork.

## Layout

```text
main.py          # Loads configuration and starts the bot
core/config.py   # Environment-backed settings
core/bot.py      # Bot class
cogs/cleanup.py  # Deletes prefix command messages
cogs/general.py  # General commands such as >ping
cogs/config.py   # The >config command group
cogs/status.py   # The >status command group
cogs/presence.py # Custom Discord presence
```
