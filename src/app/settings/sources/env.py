import os
from pathlib import Path

import environ


def read_env(env_file_path=None):
    if not env_file_path:
        root_dir = Path(os.path.dirname(os.path.realpath(__name__)))
        env_file_path = root_dir / '.env'

    environ.Env.read_env(env_file_path)
