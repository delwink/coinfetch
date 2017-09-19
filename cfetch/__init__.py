##
##  coinfetch - plugin-based cryptocurrency price converter
##  Copyright (C) 2015-2016 Delwink, LLC
##
## Redistributions, modified or unmodified, in whole or in part, must retain
## applicable copyright or other legal privilege notices, these conditions, and
## the following license terms and disclaimer.  Subject to these conditions,
## the holder(s) of copyright or other legal privileges, author(s) or
## assembler(s), and contributors of this work hereby grant to any person who
## obtains a copy of this work in any form:
##
## 1. Permission to reproduce, modify, distribute, publish, sell, sublicense,
## use, and/or otherwise deal in the licensed material without restriction.
##
## 2. A perpetual, worldwide, non-exclusive, royalty-free, irrevocable patent
## license to reproduce, modify, distribute, publish, sell, use, and/or
## otherwise deal in the licensed material without restriction, for any and all
## patents:
##
##     a. Held by each such holder of copyright or other legal privilege,
##     author or assembler, or contributor, necessarily infringed by the
##     contributions alone or by combination with the work, of that privilege
##     holder, author or assembler, or contributor.
##
##     b. Necessarily infringed by the work at the time that holder of
##     copyright or other privilege, author or assembler, or contributor made
##     any contribution to the work.
##
## NO WARRANTY OF ANY KIND IS IMPLIED BY, OR SHOULD BE INFERRED FROM, THIS
## LICENSE OR THE ACT OF DISTRIBUTION UNDER THE TERMS OF THIS LICENSE,
## INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
## A PARTICULAR PURPOSE, AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS,
## ASSEMBLERS, OR HOLDERS OF COPYRIGHT OR OTHER LEGAL PRIVILEGE BE LIABLE FOR
## ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN ACTION OF CONTRACT, TORT,
## OR OTHERWISE ARISING FROM, OUT OF, OR IN CONNECTION WITH THE WORK OR THE USE
## OF OR OTHER DEALINGS IN THE WORK.
##

from importlib.machinery import SourceFileLoader
from os import listdir
from os.path import basename, dirname, exists, expanduser, isdir, join
from os.path import realpath
from requests import get

__version__ = '5.3.0'

class NoSuchPairException(Exception):
    pass

class NoSuchKindException(Exception):
    pass

## A cryptocurrency exchange rate ticker.
class Ticker():
    ## Constructor for this class.
    #  @param path The URL prefix for this ticker.
    def __init__(self, path, kind=None):
        self.path = path

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
    def get_pair_data(self, response, pair=None):
        if type(pair) in (list, tuple):
            return response.json()[self.get_pair(pair[0], pair[1])]
        else:
            raise TypeError('pair cannot be {}'.format(type(pair)))

    ## Gets the exchange rate between two currencies raised to a power.
    #  @param a The first currency.
    #  @param b The second currency.
    #  @param amt The number quantity of 'a' currency.
    #  @param power The power to which the calculation will be raised.
    #  @param kind The type of rate to calculate.
    #  @return The exchange rate between 'a' and 'b' currencies raised to
    # 'power'.
    def get_rate_pow(self, a, b, amt, power, kind):
        r = get(self.path + self.get_pair(a, b))

        try:
            res = self.get_pair_data(r, (a, b))
        except KeyError as e:
            raise NoSuchPairException(str(e))

        if kind not in res:
            raise NoSuchKindException(kind)

        return (float(res[kind]) ** power) * amt

    ## Calculates the exchange rate between two currencies.
    #  @param a The first currency.
    #  @param b The second currency.
    #  @param amt The number quantity of 'a' currency.
    #  @param kind The type of rate to calculate.
    #  @return The exchange rate between 'a' and 'b' currencies.
    def get_rate(self, a, b, amt=1, kind='avg'):
        try:
            return self.get_rate_pow(a, b, amt, 1, kind)
        except NoSuchPairException:
            return self.get_rate_pow(b, a, amt, -1, kind)

_INDEX = {
    'description': 0,
    'value': 1
}

_PATH = [
    dirname(realpath(__file__)),
    '/usr/share/coinfetch',
    '/usr/local/share/coinfetch',
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
        SourceFileLoader('plugin', path).load_module()

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
