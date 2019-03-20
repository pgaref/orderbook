import sys


class Order(object):

    def __init__(self, order_type, order_id, order_price, order_size, order_peak_size=None):
        self.type = order_type
        self.id = order_id
        self.price = order_price
        # public size visible through the book
        self.peak_size = order_size if order_peak_size is None else order_peak_size
        self.size = order_size if order_peak_size is None else order_peak_size
        self.left_peak_size = order_size - self.peak_size
        # DList: each Order has a next and previous (see OrderList)
        self.next_order = None
        self.prev_order = None
        self.trade_size = 0  # Variable to track traded size (of matched orders)

    @property
    def is_bid(self):
        """
        Returns if the Order is a bid or not
        :return boolean:
        """
        return self.type == 'B'

    def match(self, other_order):
        """
        Returns true ONLY when other_order matches ALL current size
        :param other_order:
        :return boolean:
        """
        # Error checking
        # if other_order.type == self.type:
        #     return False
        # if other_order.is_bid and other_order.price < self.price:
        #     return False
        # if not other_order.is_bid and self.price < other_order.price:
        #     return False
        # full size trade (peak_size <= other_order.peak_size)
        if self.peak_size <= other_order.peak_size:
            new_trade_size = self.peak_size
            # update both parties
            self.make_trade(new_trade_size)
            other_order.make_trade(new_trade_size)
            return True
        # partial trade (peak_size > other_order.peak_size)
        else:
            new_trade_size = other_order.peak_size
            self.make_trade(new_trade_size)
            other_order.make_trade(new_trade_size)
            return False

    def make_trade(self, trade_size):
        """
        Close a deal of a specific size and update remaining order sizes accordingly
        :param trade_size:
        """
        self.trade_size += trade_size
        self.peak_size -= trade_size
        # Account for the remaining size (Iceberg order)
        if self.peak_size == 0 and self.left_peak_size > 0:
            if self.left_peak_size >= self.size:
                self.peak_size += self.size
            else:
                self.peak_size += self.left_peak_size
            self.left_peak_size -= self.peak_size

    def restore_peak_size(self):
        """
        Make sure when an new order is added to the book after the
        matching process the peak_size is restored (for Iceberg Orders)
        """
        if self.left_peak_size > 0 and self.peak_size < self.size:
            # Account for the left_peak_size which might be less than peak_size
            diff = min(self.size - self.peak_size, self.left_peak_size)
            self.peak_size += diff
            self.left_peak_size -= diff

    def print_trade_result(self, other_order_id):
        if self.trade_size > 0:
            if self.is_bid:
                print("{},{},{},{}".format(self.id, other_order_id, self.price, self.trade_size))
            else:
                print("{},{},{},{}".format(other_order_id, self.id, self.price, self.trade_size))
            self.trade_size = 0

    def to_print(self):
        if self.is_bid:
            sys.stdout.write("{:>10}|{:>13}|{:>7}".format(     # custom line spacing
                    self.id,
                    "{:,}".format(self.peak_size),  # thousands separator
                    "{:,}".format(self.price)))
        else:
            sys.stdout.write("{:>7}|{:>13}|{:>10}".format(
                "{:,}".format(self.price),
                "{:,}".format(self.peak_size),
                self.id))

    def __str__(self):
        return "Order: type: {} id: {} price: {} size {}".format(self.type, self.id, self.price, self.peak_size)
