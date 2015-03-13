from setuptools import setup

setup(
    name = 'coinfetch',
    version = '4.0.0',
    scripts = ['coinfetch', 'bterfetch'],
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
