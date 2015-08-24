##
##  coinfetch - plugin-based cryptocurrency price converter
##  Copyright (C) 2015 Delwink, LLC
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU Affero General Public License as published by
##  the Free Software Foundation, version 3 only.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU Affero General Public License for more details.
##
##  You should have received a copy of the GNU Affero General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from os import listdir
from os.path import dirname, exists, expanduser, isdir, join, realpath
from requests import get

__version__ = '5.0.0'

## A cryptocurrency exchange rate ticker.
class Ticker():
    ## Constructor for this class.
    #  @param path The URL prefix for this ticker.
    #  @param kind Which type of exchange rate to fetch.
    def __init__(self, path, kind='avg'):
        self.path = path
        self.kind = kind

    ## Defines how a currency pair is defined in the request URL.
    #  @param a The first currency.
    #  @param b The second currency.
    #  @return A pair string to be used in the request URL.
    def get_pair(self, a, b):
        return '{}_{}'.format(a, b)

    ## Extracts the exchange rate data from the server response.
    #  @param response Original response from the ticker server.
    #  @param The coin pair as a list/tuple.
    #  @return The data for the selected pair.
    def get_pair_data(self, response, pair):
        return response.json()[self.get_pair(pair[0], pair[1])]

    ## Calculates the exchange rate between two currencies.
    #  @param a The first currency.
    #  @param b The second currency.
    #  @param amt The number quantity of 'a' currency.
    def get_rate(self, a, b, amt=1):
        r = get(self.path + self.get_pair(a, b))

        try:
            res = self.get_pair_data(r, (a, b))
            return float(res[self.kind]) * amt
        except (KeyError, TypeError):
            try:
                r = get(self.path + self.get_pair(b, a)) # reverse order

                res = self.get_pair_data(r, (a, b))
                return (float(res[self.kind]) ** -1) * amt
            except (KeyError, TypeError) as e:
                raise ValueError(str(e)) # currency pair not found

_INDEX = {
    'description': 0,
    'value': 1
}

_PATH = [
    '/usr/share/coinfetch',
    dirname(realpath(__file__)),
    join(expanduser('~'), '.coinfetch')
]

_tickers = {}

## Adds a directory to the configuration path.
#  @param path The directory to be added.
def add_to_path(path):
    _PATH.append(path)

## Gets the registered tickers and their descriptions.
#  @return A list of tuples containing the ticker name and description.
def get_registered_tickers():
    lst = []

    for key in _tickers:
        lst.append((key, _tickers[key][_INDEX['description']]))

    return lst

## Gets a particular ticker object.
#  @param key Name of the desired ticker.
#  @return The Ticker object specified by 'key'.
def get_ticker(key):
    return _tickers[key][_INDEX['value']]

## Registers a new ticker API.
#  @param name Name of this ticker.
#  @param description A brief description of this ticker.
#  @param obj An instance of the ticker's implementation class.
def register_ticker(name, description, obj):
    _tickers[name] = (description, obj)

## Loads a plugin or directory of plugins.
#  @param path Path to the plugin file or a directory containing plugins.
def load(path):
    if isdir(path):
        for f in listdir(path):
            if f.endswith('.py'):
                load(join(path, f))
    else:
        with open(path) as plugin:
            exec(plugin.read(), globals(), locals())

## Loads all default plugins.
def load_default_plugins():
    for d in _PATH:
        plugindir = join(d, 'plugins')
        if exists(plugindir):
            load(plugindir)

## Clears the list of loaded plugins.
def unload_plugins():
    global _tickers
    _tickers = {}
