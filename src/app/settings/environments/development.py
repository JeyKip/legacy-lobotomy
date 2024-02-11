from ..sources.env import read_env

read_env()

from ..configs.base import *
from ..configs.smtp import *
from ..configs.media import *

INSTALLED_APPS = [
    *INSTALLED_APPS,
    'app'
]
