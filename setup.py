import re
from os.path import dirname, realpath

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('cfetch/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name = 'coinfetch',
    version = version,
    scripts = ['coinfetch'],
    packages = ['cfetch'],

    package_dir = {
        'cfetch': 'cfetch'
    },

    install_requires = ['requests'],

    package_data = {
        '': ['README'],
        'cfetch': ['plugins/*.py']
    },
    include_package_data=True,

    author = 'Delwink, LLC',
    author_email = 'support@delwink.com',
    description = 'Cryptocurrency price converter',
    license = 'AGPLv3',
    keywords = 'coin fetch coinfetch ticker bitcoin cryptocurrency money',
    url = 'http://delwink.com/software/coinfetch.html'
)
