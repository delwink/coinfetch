##
##  coinfetch-api-ccc - CryptoCoin Charts API plugin for coinfetch
##  Copyright (C) 2015-2016 Delwink, LLC
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

from cfetch import register_ticker, NoSuchKindException, NoSuchPairException
from cfetch import Ticker

class CccTicker(Ticker):
    def __init__(self, path):
        super().__init__(path)

    def get_pair_data(self, response, pair=None):
        return response.json()

    def get_rate_pow(self, a, b, amt, power, kind):
        r = get(self.path + self.get_pair(a, b))
        res = self.get_pair_data(r, (a, b))

        if kind not in res:
            raise NoSuchKindException(kind)

        if res[kind] is None:
            raise NoSuchPairException('{}/{}'.format(a, b))

        return (float(res[kind]) ** power) * amt

    def get_rate(self, a, b, amt=1, kind='price'):
        return super().get_rate(a, b, amt, kind)

register_ticker('ccc', 'The CryptoCoin Charts ticker (built-in)',
                CccTicker('http://api.cryptocoincharts.info/tradingPair/'))
