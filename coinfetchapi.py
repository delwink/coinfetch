#! /usr/bin/env python3
##
##  coinfetchapi - API module for coinfetch
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

from requests import get
from getopt import getopt
from sys import stderr

USAGE_INFO = '''
USAGE: coinfetch [OPTIONS] [AMOUNT] FROM TO

coinfetch will print the solution for x in the following equation:

    AMOUNT * FROM = x * TO

OPTIONS:
    -h, --help          Prints this help message.
    -v, --version       Outputs version information and exits.
    -a, --api=Y         Uses the API specified by Y.
    -k, --kind=Z        Gets the Z kind of exchange rate.

Supported APIs:
    btce                BTC-E, the default API.
    bter                BTer, the legacy API.
    ccc                 CryptoCoin Charts.

Kinds:
    avg                 Average rate, the default.
    high                The high rate.
    low                 The low rate.
    last                The last exchange amount.

Examples:
    coinfetch -k high btc usd   # gets the high rate for Bitcoin to USD
    coinfetch -a bter usd doge  # gets the average Dogecoin to USD conversion
'''

class UsageException(Exception):
    pass

def print_usage(e):
    print(USAGE_INFO)
    exit(int(str(e)))

def _keypair(api, r, pair):
    if api in ('btce'):
        return r.json()[pair]
    elif api in ('bter', 'ccc'):
        return r.json()

    raise ValueError('API %s not supported.' %api)

def get_rate(coin_a, coin_b, amt, api, kind):
    if api == 'btce':
        url = 'https://btc-e.com/api/3/ticker/'
    elif api == 'bter':
        url = 'http://data.bter.com/api/1/ticker/'
    elif api == 'ccc':
        url = 'http://api.cryptocoincharts.info/tradingPair/'
        if kind == 'avg':
            kind = 'price'
        else:
            raise ValueError('kind %s not supported with API %s' %(kind, api))
    else:
        raise ValueError('API %s not supported.' %api)

    pair = '%s_%s' %(coin_a, coin_b)

    r = get(url + pair)

    try:
        res = _keypair(api, r, pair)
        return float(res[kind]) * amt
    except (KeyError, TypeError):
        try:
            pair = '%s_%s' %(coin_b, coin_a)
            r = get(url + pair)

            res = _keypair(api, r, pair)
            return (float(res[kind]) ** -1) * amt
        except TypeError as e:
            raise ValueError('currency pair not found: %s' %str(e))

def coinfetch(args):
    api = 'btce'
    kind = 'avg'
    opts, args = getopt(args, "hva:k:", ['help', 'version', 'api=', 'kind='])

    for key, value in opts:
        if key in ('-h', '--help'):
            raise UsageException(0)
        elif key in ('-v', '--version'):
            print('''coinfetch 4.1.1
Copyright (C) 2015 Delwink, LLC
License AGPLv3: GNU AGPL version 3 only <http://gnu.org/licenses/agpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by David McMackins II''')
            exit(0)
        elif key in ('-a', '--api'):
            api = value
        elif key in ('-k', '--kind'):
            kind = value

    bump = 1 if len(args) == 3 else 0
    amt = float(args[0]) if len(args) == 3 else 1.0

    try:
        print('%.8f' %get_rate(args[bump], args[1+bump], amt, api, kind))
    except IndexError:
        raise UsageException(1)
    except KeyError as e:
        print('coinfetch: currency pair not found: %s' %str(e), file=stderr)
        exit(2)
    except ValueError as e:
        print('coinfetch: %s' %str(e), file=stderr)
        exit(3)
