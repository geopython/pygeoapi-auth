###################################################################
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2024 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
###################################################################

from abc import ABC, abstractmethod
import importlib
import logging
from typing import IO

import yaml

LOGGER = logging.getLogger(__name__)


class AuthProvider(ABC):
    def __init__(self, config: IO = None):
        """Initializer"""

        self.config = yaml.safe_load(config)
        self.resources = self.get_resources()

    @abstractmethod
    def get_resources(self):
        raise NotImplementedError()

    @abstractmethod
    def is_resource_protected(
            self, path: str, api_prefix: str = None) -> bool:

        raise NotImplementedError()


def load_auth_provider(factory: str, config_file: str) -> AuthProvider:
    """
    Load auth provider plugin

    :param factory: `str` of dotted path of Python module/class
    :param configuration: `str` of configuration of auth provider

    :returns: AuthProvider object
    """

    modulename = f'{__package__}.{factory}'
    classname = AUTH_PROVIDERS[factory]

    LOGGER.debug(f'module name: {modulename}')
    LOGGER.debug(f'class name: {classname}')

    module = importlib.import_module(modulename)

    return getattr(module, classname)(config_file)


AUTH_PROVIDERS = {
    'authelia': 'AutheliaAuthProvider'
}
