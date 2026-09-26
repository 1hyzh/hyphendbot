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
```

`delete_after` controls how long prefix command messages and explicitly scheduled command responses remain visible. Set it to `0` or a negative value to disable deletion.

Runtime configuration commands:

```text
>help
>health
>config
>config prefix !
>config delete_after 5
>config readall_limit 25
>config rpc Listening to music
>config rpc_type listening
>rpc text Listening to music
>rpc type listening
>status dnd
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
Command responses are plain text with a `- ` style prefix. Help and health responses include a `# hyphend bot` watermark and the bot version.

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
