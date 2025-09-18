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

import logging
import re

from pygeoapi_auth.auth import AuthProvider

LOGGER = logging.getLogger(__name__)


class AutheliaAuthProvider(AuthProvider):
    def get_resources(self):
        return [item for sublist in self.config['access_control']['rules']
                for item in sublist['resources']]

    def is_resource_protected(self, path: str, api_prefix: str = None) -> bool:
        for resource in self.resources:
            LOGGER.debug(f'Testing {path} against {resource}')
            if api_prefix is not None:
                path2 = f'/{api_prefix}{path}'
            else:
                path2 = path

            LOGGER.debug(f'Generated path: {path2}')

            if re.search(resource, path2):
                LOGGER.debug(f'{path2} matches {resource}')
                return True

        return False
