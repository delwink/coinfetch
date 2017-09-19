##
##  coinfetch-api-cb - Coinbase API plugin for coinfetch
##  Copyright (C) 2017 Delwink, LLC
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

from cfetch import register_ticker, NoSuchKindException, NoSuchPairException
from cfetch import Ticker

class CoinbaseTicker(Ticker):
    def __init__(self, path):
        super().__init__(path)

    def get_pair(self, a, b):
        return '{}-{}'.format(a.upper(), b.upper())

    def get_pair_data(self, response, pair=None):
        return response.json()

    def get_rate_pow(self, a, b, amt, power, kind):
        if kind not in ('spot', 'buy', 'sell'):
            raise NoSuchKindException(kind)

        r = get(self.path + self.get_pair(a, b) + '/' + kind,
                headers={'CB-VERSION': '2017-09-19'})

        res = self.get_pair_data(r, (a, b))
        print(r.text)
        if 'data' not in res:
            raise NoSuchPairException('{}/{}'.format(a, b))

        if 'errors' in res:
            raise Exception(res['errors'])

        return (float(res['data']['amount']) ** power) * amt

    def get_rate(self, a, b, amt=1, kind='spot'):
        return super().get_rate(a, b, amt, kind)

register_ticker('cb', 'The Coinbase ticker (built-in)',
                CoinbaseTicker('https://api.coinbase.com/v2/prices/'))
