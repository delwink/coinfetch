##
##  coinfetch-api-btce - BTC-E API plugin for coinfetch
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

from coinfetch import register_ticker, Ticker

register_ticker('btc-e', 'The BTC-E ticker',
                Ticker('https://btc-e.com/api/3/ticker/'))
