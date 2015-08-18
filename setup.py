import re
from setuptools import setup

version = ''
with open('coinfetchapi.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name = 'coinfetch',
    version = version,
    scripts = ['coinfetch', 'bterfetch', 'cccfetch'],
    py_modules = ['coinfetchapi'],

    install_requires = ['requests'],

    package_data = {
        '': ['README']
    },

    author = 'Delwink, LLC',
    author_email = 'support@delwink.com',
    description = 'Cryptocurrency price converter',
    license = 'AGPLv3',
    keywords = 'coin fetch coinfetch ticker bitcoin cryptocurrency money',
    url = 'http://delwink.com/software/coinfetch.html'
)
