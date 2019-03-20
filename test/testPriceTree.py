import unittest

from orderbook.src.common.order import Order
from orderbook.src.common.priceTree import PriceTree
from orderbook.src.common.ptreeIterator import ComplexIterator


class TestPriceTree(unittest.TestCase):

    def test_PriceTreeInsert(self):
        num_elements = 5
        price_tree = TestPriceTree.populate_tree(num_elements)
        self.assertTrue(len(price_tree.price_map) == num_elements)
        self.assertTrue(price_tree.max == num_elements-1)
        self.assertTrue(price_tree.min == 0)

    def test_PriceTreeIterator(self):
        ptree = PriceTree('test')
        ptree.insert_price_order(Order('B', 1, 5000, 7500))
        ptree.insert_price_order(Order('B', 2, 5000, 7500))
        # Same TreeNode Iteration
        it = ComplexIterator(ptree.tree.values())
        count = 0
        while it.hasnext():
            next(it)
            count += 1
        self.assertTrue(count == 2)
        # Adding a separate TreeNode (different price)
        ptree.insert_price_order(Order('B', 3, 6000, 7500))
        ptree.insert_price_order(Order('B', 4, 6000, 7500))
        it = ComplexIterator(ptree.tree.values())
        count = 0
        while it.hasnext():
            next(it)
            count += 1
        self.assertTrue(count == 4)

    def test_PriceTreeDelete(self):
        ptree = PriceTree('test')
        ptree.insert_price_order(Order('B', 1, 5000, 7500))
        ptree.insert_price_order(Order('B', 2, 6000, 7500))
        ptree.insert_price_order(Order('B', 3, 5000, 7500))
        ptree.insert_price_order(Order('B', 4, 6000, 7500))

        # Two different prices
        self.assertTrue(ptree.price_map.__len__() == 2)
        # Four different orders
        self.assertTrue(ptree.order_map.__len__() == 4)
        # Another two orders
        ptree.remove_price(6000)
        self.assertTrue(ptree.price_map.__len__() == 1)
        self.assertTrue(ptree.order_map.__len__() == 2)
        # Remove the rest
        ptree.remove_price(5000)
        self.assertTrue(ptree.price_map.__len__() == 0)
        self.assertTrue(ptree.order_map.__len__() == 0)


    @staticmethod
    def populate_tree(num_elements):
        price_tree = PriceTree('test')
        for i in range(0, num_elements):
            price_tree.insert_price(i)
        return price_tree
