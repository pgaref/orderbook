import unittest

from orderbook.src.common.order import Order


class TestOrder(unittest.TestCase):

    def test_LimitOrderSimple(self):
        # B, 100322, 5103, 7500
        # Limit order id 100322: Buy 7,500 at 5,103p,
        order_type = 'B'
        order_id = 100322
        order_price = 5103
        order_size = 7500
        order = Order(order_type, order_id, order_price, order_size)
        self.assertTrue(order.is_bid)
        self.assertEqual(order.type, 'B')
        self.assertEqual(order.id, order_id)
        self.assertEqual(order.price, order_price)
        self.assertEqual(order.peak_size, order_size)
        self.assertEqual(order.size, order_size)
        self.assertTrue(order.left_peak_size == 0)
        self.assertEqual(order.__str__(), "Order: type: {} id: {} price: {} size {}".format(order_type, order_id, order_price, order_size))

    def test_IcebergOrderSimple(self):
        # S, 100345, 5103, 100000, 10000
        # Iceberg order id 100345: Sell 100,000 at 5103p, with a peak size of 10,000
        order_type = 'S'
        order_id = 100345
        order_price = 5103
        order_size = 100000
        order_peak = 10000
        order = Order(order_type, order_id, order_price, order_size, order_peak)
        self.assertTrue(not order.is_bid)
        self.assertEqual(order.type, 'S')
        self.assertEqual(order.id, order_id)
        self.assertEqual(order.price, order_price)
        self.assertEqual(order.peak_size, order_peak)
        self.assertEqual(order.size, order_peak)
        self.assertTrue(order.left_peak_size == 90000)

    def test_makeTrade(self):
        order_type = 'S'
        order_id = 100345
        order_price = 5103
        order_size = 100000
        order_peak = 10000
        ice_order = Order(order_type, order_id, order_price, order_size, order_peak)
        # Remaining public size
        ice_order.make_trade(5000)
        self.assertTrue(ice_order.peak_size == 5000)
        self.assertTrue(ice_order.left_peak_size == 90000)
        self.assertTrue(ice_order.trade_size == 5000)

        ice_order = Order(order_type, order_id, order_price, order_size, order_peak)
        # No remaining public size - should deduct from leftpeak
        ice_order.make_trade(10000)
        self.assertTrue(ice_order.peak_size == 10000)
        self.assertTrue(ice_order.left_peak_size == 80000)
        self.assertTrue(ice_order.trade_size == 10000)

        # To empty final Order
        ice_order = Order(order_type, order_id, order_price, 5000)
        ice_order.make_trade(5000)
        self.assertTrue(ice_order.peak_size == 0)
        self.assertTrue(ice_order.left_peak_size == 0)
        self.assertTrue(ice_order.trade_size == 5000)

        # TODO Trades above peak should never happen - check?
        ice_order = Order(order_type, order_id, order_price, 5000)
        ice_order.make_trade(10000)


if __name__ == '__main__':
    unittest.main()
