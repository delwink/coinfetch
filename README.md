coinfetch
=========

A python script that is capable of printing almost all cryptocoin prices in terms 
of other coins (and fiat money).

Using coinfetch
---------------

coinfetch takes two arguments from the command line, and returns a conversion factor.

The arguments are the three (or sometimes four) letter identifiers of various currencies.

Many (but not all) pairs of coins can be used.

Example: <code>$ coinfetch doge btc</code>

The above example will return the amount of Bitcoin that can currently be bought with one
Dogecoin. 

If the coins are reversed (e.g. <code>$ coinfetch btc doge</code> ), the amount of Dogecoin
that can currently be bought with one Bitcoin will be returned.

Installation
------------

To install coinfetch:

<code>$ chmod +x ./coinfetch && sudo cp ./coinfetch /usr/local/bin/</code>

Licensing
---------

This script is [free software](http://gnu.org/philosophy/free-sw.html), licensed
under the terms of the MIT license. See [LICENSE](LICENSE) for more information.
