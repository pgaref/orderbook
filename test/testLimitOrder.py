import unittest

from orderbook.src.common.order import Order
from orderbook.src.orderBook import OrderBook


class TestLimitOrder(unittest.TestCase):

    def test_LimitOrderSimple(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 101, 10))
        book.process_order(Order('B', 2, 101, 10))
        trades = book.process_order(Order('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)
        # Marching first B order
        trades = book.process_order(Order('S', 4, 101, 10))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 1)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)

    def test_LimitOrdersAdvanced(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 101, 10))
        book.process_order(Order('B', 2, 101, 10))
        trades = book.process_order(Order('S', 3, 103, 10))
        self.assertTrue(len(trades) == 0)
        # Fill both B orders
        trades = book.process_order(Order('S', 5, 101, 20))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)

    def test_LimitOrderPartial(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 101, 10))
        book.process_order(Order('B', 2, 101, 10))
        trades = book.process_order(Order('S', 5, 101, 15))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 1)
        self.assertTrue(len(book.asks.price_map) == 0)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)
        self.assertTrue(trades[1].peak_size == 5)

    def test_LimitNewOrderPartial(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 101, 10))
        book.process_order(Order('B', 2, 101, 10))
        trades = book.process_order(Order('S', 5, 101, 25))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 0)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(trades[1].id == 2)
        self.assertTrue(book.asks.order_map[5].peak_size == 5)

    if __name__ == '__main__':
        unittest.main()
