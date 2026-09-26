import os
from dataclasses import dataclass


def env_value(name: str, default: str = '') -> str:
    return os.getenv(name) or os.getenv(name.upper(), default)


@dataclass
class Config:
    wt: str
    token: str
    prefix: str
    delete_after: float
    custom_rpc: str
    custom_rpc_type: str
    custom_rpc_url: str
    status: str
    readall_delay: float
    readall_limit: int

    @classmethod
    def from_environment(cls) -> 'Config':
        token = env_value('token').strip()
        if not token:
            raise RuntimeError('Add a non-empty token value to env.')

        return cls(
            wt=env_value('# hyphendbot', 'v0.1.0'),
            token=token,
            prefix=env_value('prefix', '>'),
            delete_after=float(env_value('delete_after', '10')),
            custom_rpc=env_value('custom_rpc', 'hyphendbot'),
            custom_rpc_type=env_value('custom_rpc_type', 'playing').lower(),
            custom_rpc_url=env_value('custom_rpc_url'),
            status=env_value('status', 'online').lower(),
            readall_delay=max(0.0, float(env_value('readall_delay', '2'))),
            readall_limit=max(1, int(env_value('readall_limit', '25'))),
        )