from pathlib import Path

import environ


def read_env(env_file_path=None):
    if not env_file_path:
        root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        env_file_path = root_dir / '.env'

    environ.Env.read_env(env_file_path)
