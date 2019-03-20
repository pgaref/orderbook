import unittest

from orderbook.src.common.order import Order
from orderbook.src.orderBook import OrderBook


class TestIcebergOrder(unittest.TestCase):

    def test_AggessiveIcebergOrder(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 99, 50, 50000))
        book.process_order(Order('B', 2, 98, 25, 25500))
        book.process_order(Order('S', 3, 100, 25, 10000))
        book.process_order(Order('S', 4, 100, 25, 7500))
        trades = book.process_order(Order('S', 5, 101, 25, 20000))
        self.assertTrue(len(trades) == 0)
        # Fill twp sell orders with an iceberg
        trades = book.process_order(Order('B', 6, 100, 100000, 10000))
        self.assertTrue(len(trades) == 2)
        self.assertTrue(len(book.bids.price_map) == 3)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 3)
        self.assertTrue(trades[1].id == 4)
        self.assertTrue(book.bids.order_map[6].left_peak_size == 72500)
        self.assertTrue(book.bids.order_map[6].peak_size == 10000)

    def test_PassiveIcebergOder(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 100, 82500, 10000))
        book.process_order(Order('B', 2, 99, 50000))
        book.process_order(Order('B', 3, 98, 25500))
        book.process_order(Order('S', 4, 101, 20000))
        trades = book.process_order(Order('S', 5, 100, 10000))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 3)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(book.bids.order_map[1].left_peak_size == 62500)
        self.assertTrue(book.bids.order_map[1].peak_size == 10000)

    def test_PassiveIcebergPeak(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 100, 72500, 10000))
        book.process_order(Order('B', 2, 99, 50000))
        book.process_order(Order('B', 3, 98, 25500))
        book.process_order(Order('S', 4, 101, 20000))
        trades = book.process_order(Order('S', 5, 99, 11000))
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 3)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        # Leftovers should be peak - 1k
        self.assertTrue(book.bids.order_map[1].left_peak_size == 52500)
        self.assertTrue(book.bids.order_map[1].peak_size == 9000)

    def test_passiveIcebergTwoOrders(self):
        book = OrderBook()
        book.process_order(Order('B', 1, 100, 72500, 10000))
        book.process_order(Order('B', 2, 99, 50000))
        book.process_order(Order('B', 3, 98, 25500))
        book.process_order(Order('S', 4, 101, 20000))
        trades = book.process_order(Order('S', 5, 99, 35000))
        # Match the max - 35k from 1
        self.assertTrue(len(trades) == 1)
        self.assertTrue(len(book.bids.price_map) == 3)
        self.assertTrue(len(book.asks.price_map) == 1)
        self.assertTrue(trades[0].id == 1)
        self.assertTrue(book.bids.order_map[1].left_peak_size == 32500)
        self.assertTrue(book.bids.order_map[1].peak_size == 5000)

    if __name__ == '__main__':
        unittest.main()
