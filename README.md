# hyphendbot

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The bot reads configuration from the `env` file:

```env
token=your-discord-token
prefix=>
delete_after=10
custom_rpc=hyphendbot
custom_rpc_type=playing
custom_rpc_url=
status=online
lastfm_api_key=
lastfm_username=
lastfm_poll_seconds=60
```

`delete_after` controls how long prefix command messages and explicitly scheduled command responses remain visible. Set it to `0` or a negative value to disable deletion.

Runtime configuration commands:

```text
>config
>config prefix !
>config delete_after 5
>config rpc Listening to music
>config rpc_type listening
>rpc text Listening to music
>rpc type listening
>status dnd
```

Every response sent through a command context, including help output, uses the configured deletion delay.

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
cogs/lastfm.py   # Last.fm now-playing presence
```
