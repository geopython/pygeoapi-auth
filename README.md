# pygeoapi-auth

Python module to manage pygeoapi authorization

## Installation

pygeoapi-auth is best installed and used within a Python virtualenv.

### Requirements

* Python 3 and above
* Python [virtualenv](https://virtualenv.pypa.io) package

### Dependencies

Dependencies are listed in [requirements.txt](requirements.txt). Dependencies
are automatically installed during pygeoapi-auth's installation.

### Installing the Package

```bash
python3 -m venv my-env
cd my-env
. bin/activate
git clone https://github.com/cartologic/pygeoapi-auth.git
cd pygeoapi-auth
python3 setup.py install
```

## Running

### From the command line

```bash
# show all subcommands
pygeoapi-auth

# inject authorization into OpenAPI using Authelia
pygeoapi-auth openapi inject-auth local-openapi.yml authelia authelia-conf.yml

# inject authorization into OpenAPI using Authelia with an API prefix
pygeoapi-auth openapi inject-auth local-openapi.yml authelia authelia-conf.yml --api-prefix api 

# inject authorization into OpenAPI using Authelia with an API prefix, writing to file
pygeoapi-auth openapi inject-auth local-openapi.yml authelia authelia-conf.yml --api-prefix api --output-file openapi-auth.yml

# if installed in the pygeoapi deployment environment, run as a plugin!
pygeoapi plugins openapi inject-auth local-openapi.yml authelia authelia-conf.yml --api-prefix api --output-file openapi-auth.yml
```

### Using the API from Python

TODO

## Development

### Setting up a Development Environment

Same as installing a package.  Use a virtualenv.  Also install developer
requirements:

```bash
pip3 install -r requirements-dev.txt
```

### Running Tests

```bash
# via setuptools
python3 setup.py test
# manually
cd tests
python3 run_tests.py
```

## Releasing

```bash
# update version
vi pygeoapi_auth/__init__.py
git commit -m 'update release version' pygeoapi_auth/__init__.py
# push changes
git push origin master
git tag -a x.y.z -m 'tagging release x.y.z'
# push tag
git push --tags
rm -fr build dist *.egg-info
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

### Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

### Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/geopython/pygeoapi-auth/issues).

## Contact

* [Tom Kralidis](https://github.com/tomkralidis)
* [Youssef Harby](https://github.com/Youssef-Harby)
