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
    readall_delay: float
    readall_limit: int

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
            readall_delay=max(0.0, float(os.getenv('readall_delay', '2'))),
            readall_limit=max(1, int(os.getenv('readall_limit', '25'))),
        )