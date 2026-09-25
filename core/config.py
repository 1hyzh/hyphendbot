import os
from dataclasses import dataclass


@dataclass
class Config:
    token: str
    prefix: str
    delete_after: float
    custom_rpc: str
    custom_rpc_type: str
    custom_rpc_url: str
    status: str
    lastfm_api_key: str
    lastfm_username: str
    lastfm_poll_seconds: float

    @classmethod
    def from_environment(cls) -> 'Config':
        token = os.getenv('token', '').strip()
        if not token:
            raise RuntimeError('Add a non-empty token value to env.')

        return cls(
            token=token,
            prefix=os.getenv('prefix', '>'),
            delete_after=float(os.getenv('delete_after', '10')),
            custom_rpc=os.getenv('custom_rpc', 'hyphendbot'),
            custom_rpc_type=os.getenv('custom_rpc_type', 'playing').lower(),
            custom_rpc_url=os.getenv('custom_rpc_url', ''),
            status=os.getenv('status', 'online').lower(),
            lastfm_api_key=os.getenv('lastfm_api_key', '').strip(),
            lastfm_username=os.getenv('lastfm_username', '').strip(),
            lastfm_poll_seconds=float(os.getenv('lastfm_poll_seconds', '60')),
        )