import unittest

from orderbook.src.common.order import Order
from orderbook.src.orderBook import OrderBook


class TestOrderBook(unittest.TestCase):

    def test_OrderBookAdd(self):
        book = OrderBook()
        # Simple Limit order example (as defined in spec)
        # B,100322,5103,7500
        book.process_order(Order('B', 100322, 5103, 7500))
        self.assertTrue(len(book.bids.order_map) == 1)
        self.assertTrue(100322 in book.bids.order_map)
        self.assertTrue(5103 is book.bids.max)
        self.assertTrue(5103 in book.bids.price_map)

        # Simple Iceberg order example (as defined in spec)
        # S,100345,5103,100000,10000
        book.process_order(Order('S', 100345, 5103, 100000, 10000))
        self.assertTrue(len(book.asks.order_map) == 1)
        self.assertTrue(100345 in book.asks.order_map)
        # Trade should have matched the bid
        self.assertTrue(5103 is book.asks.min)
        self.assertTrue(5103 not in book.bids.price_map)

    def test_OrderBookBids(self):
        book = OrderBook()
        book.process_order(Order('B', 100322, 5103, 7500))
        book.process_order(Order('B', 100345, 5103, 10000, 100000))
        book.process_order(Order('B', 1, 5100, 10))
        self.assertTrue(len(book.bids.price_map.keys()) == 2)
        self.assertTrue(len(book.bids.order_map.keys()) == 3)
        self.assertTrue(book.bids.min == 5100)

    def test_OrberBookComplexOrders(self):
        book = OrderBook()
        book.process_order(Order('B', 1138, 31502, 7500))
        book.process_order(Order('B', 1139, 31502, 7500))
        trades = book.process_order(Order('S', 1, 31501, 20000, 800))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(trades[0].id == 1138)
        self.assertTrue(trades[1].id == 1139)
        self.assertTrue(1138 not in book.bids.order_map)
        self.assertTrue(1139 not in book.bids.order_map)
        book.process_order(Order('S', 2, 30501, 1000, 800))
        book.process_order(Order('S', 3, 30501, 200))
        trades = book.process_order(Order('B', 1003, 30501, 1000))
        self.assertTrue(3 not in book.bids.order_map)
        self.assertTrue(len(trades) == 2)
        self.assertTrue(trades[0].id == 3)
        self.assertTrue(trades[1].id == 2)

    if __name__ == '__main__':
        unittest.main()
