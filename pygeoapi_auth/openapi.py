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

import click
import yaml

from pygeoapi_auth import cli_options, util
from pygeoapi_auth.auth import load_auth_provider

LOGGER = logging.getLogger(__name__)


@click.group()
def openapi():
    """OpenAPI management"""
    pass


@click.command()
@click.pass_context
@click.argument('openapi_file', type=click.File(encoding='utf-8'))
@click.argument('auth_type')
@click.argument('auth_config_file', type=click.File(encoding='utf-8'))
@click.option('--api-prefix', help='API prefix/basepath')
@click.option('--output-file', '-of', type=click.File('w', encoding='utf-8'),
              help='Name of output file')
@cli_options.OPTION_VERBOSITY
def inject_auth(ctx, openapi_file, auth_type, auth_config_file, api_prefix,
                output_file, verbosity):

    auth_provider = load_auth_provider(auth_type, auth_config_file)

    click.echo(f'Opening {openapi_file.name}')
    o = yaml.safe_load(openapi_file)

    o['components']['securitySchemes'] = {
        'BasicAuth': {
            'type': 'http',
            'scheme': 'basic'
        }
    }

    for key, value in o['paths'].items():
        LOGGER.debug(f'Inspecting path {key}')
        if auth_provider.is_resource_protected(key, api_prefix):
            LOGGER.debug('Path is protected')
            if key == f'/{api_prefix}/':
                o['security'] = [{'BasicAuth': []}]

            for key2, value2 in value.items():
                if key2 in util.HTTP_METHODS:
                    value2['security'] = [{'BasicAuth': []}]

    content = yaml.safe_dump(o, default_flow_style=False)

    if output_file is None:
        click.echo(content)
    else:
        click.echo(f'Generating {output_file.name}')
        output_file.write(content)
        click.echo('Done')


openapi.add_command(inject_auth)
