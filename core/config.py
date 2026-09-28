import os
from dataclasses import dataclass


def env_value(name: str, default: str = '') -> str:
    return os.getenv(name) or os.getenv(name.upper(), default)


@dataclass
class Config:
    token: str
    prefix: str
    delete_after: float
    custom_rpc: str
    custom_rpc_type: str
    custom_rpc_url: str
    status: str
    readall_delay: float
    readall_limit: int
    lastfm_api_key: str
    lastfm_username: str
    lastfm_poll_interval: float
    lastfm_application_id: str
    lastfm_image_key: str

    @classmethod
    def from_environment(cls) -> 'Config':
        token = env_value('token').strip()
        if not token:
            raise RuntimeError('Add a non-empty token value to env.')

        return cls(
            token=token,
            prefix=env_value('prefix', '>'),
            delete_after=float(env_value('delete_after', '10')),
            custom_rpc=env_value('custom_rpc', 'hyphendbot'),
            custom_rpc_type=env_value('custom_rpc_type', 'playing').lower(),
            custom_rpc_url=env_value('custom_rpc_url'),
            status=env_value('status', 'online').lower(),
            readall_delay=max(0.0, float(env_value('readall_delay', '2'))),
            readall_limit=max(1, int(env_value('readall_limit', '25'))),
            lastfm_api_key=env_value('lastfm_api_key').strip(),
            lastfm_username=env_value('lastfm_username').strip(),
            lastfm_poll_interval=max(30.0, float(env_value('lastfm_poll_interval', '60'))),
            lastfm_application_id=env_value('lastfm_application_id').strip(),
            lastfm_image_key=env_value('lastfm_image_key').strip(),
        )