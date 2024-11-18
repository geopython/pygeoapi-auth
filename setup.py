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

from pathlib import Path
from setuptools import Command, find_packages, setup
import re
import sys


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        errno = subprocess.call([sys.executable, 'tests/run_tests.py'])
        raise SystemExit(errno)


def read(filename) -> str:
    """read file contents"""

    fullpath = Path(__file__).resolve().parent / filename

    with fullpath.open() as fh:
        contents = fh.read().strip()

    return contents


def get_package_version():
    """get version from top-level package init"""

    version_file = read('pygeoapi_auth/__init__.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


LONG_DESCRIPTION = read('README.md')

DESCRIPTION = 'pygeoapi-auth is a Python package to manage OpenAPI authentication definitions'  # noqa

MANIFEST = Path('MANIFEST')

if MANIFEST.exists():
    MANIFEST.unlink()

setup(
    name='pygeoapi-auth',
    version=get_package_version(),
    description=DESCRIPTION.strip(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    platforms='all',
    keywords=' '.join([
        'OpenAPI',
        'auth'
    ]),
    author='Tom Kralidis',
    author_email='tomkralidis@gmail.com',
    maintainer='Tom Kralidis',
    maintainer_email='tomkralidis@gmail.com',
    url='https://github.com/geopython/pygeoapi-auth',
    install_requires=read('requirements.txt').splitlines(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pygeoapi-auth=pygeoapi_auth:cli'
        ],
        'pygeoapi': [
            'pygeoapi-auth-openapi=pygeoapi_auth.openapi:openapi'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    cmdclass={'test': PyTest},
    test_suite='tests.run_tests'
)
