from setuptools import setup


setup(
    name = 'coinfetch',
    version = '3.0.0',
    scripts = ['coinfetch'],

    install_requires = ['requests'],

    package_data = {
        '': ['README']
    },

    author = 'Delwink, LLC',
    author_email = 'support@delwink.com',
    description = 'Cryptocurrency price converter',
    license = 'MIT',
    keywords = 'coin fetch coinfetch ticker bitcoin cryptocurrency money',
    url = 'http://delwink.com/software/coinfetch.html'
)
