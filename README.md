# OrderBook
OrderBook Simulator with Limit and Iceberg functionality

## Design
Proof of concept of a Limit Order Book (LOB)
where the bid and ask order books are implemented as separate trees.
Inspired by the [Limit Book] blog post by Selph where limit levels
are stored as nodes inside the trees and each node is a doubly-linked list of orders, sorted chronologically.

## Structure
* Source code stored under `orderbook/src/`
* Tests stored under `test/`

## Install
* `python setup.py install`

## Run
* `runner.py < data/ordersSimple.dat`

## Test
* Single: `python -m unittest test.testPriceTree`
* All: `python -m unittest discover`


## Notes
* An order book is an electronic list of buy and sell orders for a security or other instrument organized by price level
* Order books are used by almost every exchange for various assets like stocks, bonds, currencies, and even cryptocurrencies
* These lists help improve market transparency as they provide information on price, availability, depth of trade, and who initiates transactions
* There are three parts to an order book: buy orders, sell orders, and order history
* => A limit order to sell is called an "ask".
* Iceberg order is a conditional request made to the broker/system to buy or sell a large required quantity of stock, but in smaller predetermined quantity

## Best practices
*  Separate the intentions of a trading model–such as “place limit orders at $10.15 and $10.10″ from the resulting actual positions
*  The data structure chosen to represent the limit order book will be the primary source of market information



## References
* [OrderBook](https://www.investopedia.com/terms/o/order-book.asp)
* [OrderBook Programming](https://web.archive.org/web/20161116104649/http://rgmadvisors.com/problems/orderbook/)
* [Building a Trading System](https://web.archive.org/web/20110219163418/http://howtohft.wordpress.com/2011/02/15/building-a-trading-system-general-considerations/)
* [Limit Book](https://web.archive.org/web/20110219163448/http://howtohft.wordpress.com/2011/02/15/how-to-build-a-fast-limit-order-book/)
