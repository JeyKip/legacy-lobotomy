import os
from ..sources.env import read_env

read_env(f'{os.path.dirname(os.path.realpath(__name__))}/.env.testing')

from ..configs.base import *
from ..configs.media import *
from ..configs.silk import *

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
