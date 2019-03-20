import unittest

from orderbook.src.common.order import Order
from orderbook.src.common.orderList import OrderList


class TestOrderList(unittest.TestCase):

    def test_OrderListAdd(self):
        num_elements = 1000
        order_type = 'B'
        order_id = 1
        order_price = 5000
        order_size = 7500
        order_list = OrderList()
        for i in range(0, num_elements):
            order = Order(order_type, order_id, order_price, order_size, order_size)
            if order_list.tail is not None:
                self.assertTrue(order_list.tail.id < order.id)
            order_list.add(order)
            order_id += 1
        self.assertTrue(order_list.size == num_elements)

    def test_OrderListRemove(self):
        num_elements = 10
        order_list = TestOrderList.populateList(num_elements)
        self.assertTrue(order_list.size == num_elements)

        # Remove Tail (9 elements)
        order_list.remove_tail()
        self.assertTrue(order_list.tail.id == num_elements-1)
        self.assertTrue(order_list.size == num_elements-1)

        # Remove Head (8 elements)
        order_list.remove_head()
        self.assertTrue(order_list.head.id == 2)
        self.assertTrue(order_list.size == num_elements - 2)

        # Remove all
        for i in range(8, 0, -1):
            self.assertTrue(order_list.size == i)
            order_list.remove_head()
        self.assertTrue(order_list.size == 0)
        self.assertTrue(order_list.head is None)
        self.assertTrue(order_list.tail is None)

    def test_OrderListIterate(self):
        num_elements = 10
        order_list = TestOrderList.populateList(num_elements)
        self.assertTrue(order_list.size == num_elements)
        # Test iterator
        self.assertTrue(iter(order_list) is not None)
        # start from head
        start_id = 1
        for ele in order_list:
            self.assertTrue(ele.id == start_id)
            start_id += 1

    @staticmethod
    def populateList(num_elements):
        order_type = 'S'
        order_id = 1
        order_price = 5000
        order_size = 7500
        order_list = OrderList()
        # Adding num_elements
        for i in range(0, num_elements):
            order = Order(order_type, order_id, order_price, order_size)
            order_list.add(order)
            order_id += 1
        return order_list


if __name__ == '__main__':
    unittest.main()
