coinfetch
=========

See [INSTALL](INSTALL) for installation instructions.

Using `coinfetch`
-----------------

coinfetch takes two arguments from the command line, and returns a conversion 
factor.

The arguments are the three (or sometimes four) letter identifiers of various 
currencies.

Many (but not all) pairs of coins can be used.

Example: `$ coinfetch doge btc`

The above example will return the amount of Bitcoin that can currently be bought
with one Dogecoin. 

If the coins are reversed (e.g. `$ coinfetch btc doge`), the amount of Dogecoin
that can currently be bought with one Bitcoin will be returned.

As of version 2.x, you may optionally add a third argument before the first
currency in order to multiply that amount.

Example: `$ coinfetch 1000 doge usd`

The above example will return the value of 1000 DOGE in USD.

Known Bugs
----------

As of version 2.1, `coinfetch`'s measures to avoid `0.0` returns and
`Currency pair not found` errors can return inconsistent values. This is a
reality of the system that cannot be avoided. For example, getting the price for
LTC to DOGE will return a reasonable amount. However, getting the price for that
many DOGE to USD does not equal the price of 1 LTC in USD. This is a compromise
in exchange for fewer failures. These attempts to outsmart the API can create
erroneous responses, but we prefer to have rough values than no values. We may
consider adding an option to fail instead in the future (or if sponsored).

Licensing
---------

This script is [free software](http://gnu.org/philosophy/free-sw.html), licensed
under the terms of the MIT license. See [LICENSE](LICENSE) for more information.
