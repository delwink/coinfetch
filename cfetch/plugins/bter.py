##
##  coinfetch-api-bter - BTer API plugin for coinfetch
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
from requests import get

class BterTicker(Ticker):
    def get_pair_data(self, response, pair=None):
        return response.json()

    def get_rate_pow(self, a, b, amt, power, kind):
        r = get(self.path + self.get_pair(a, b))
        res = self.get_pair_data(r)

        if kind not in res:
            if res['result'] == 'false':
                raise NoSuchPairException('{}/{}'.format(a, b))

            raise NoSuchKindException(kind)

        return (float(res[kind]) ** power) * amt

register_ticker('bter', 'The BTer ticker (built-in)',
                BterTicker('http://data.bter.com/api/1/ticker/'))
