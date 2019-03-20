import sys
from orderbook.src.common.priceTree import PriceTree
from orderbook.src.common.ptreeIterator import ComplexIterator


class OrderBook(object):
    def __init__(self):
        self.bids = PriceTree('Bids')
        self.asks = PriceTree('Asks')

    def process_order(self, curr_order):
        """
        Generic method to process a Bid or Ask order
        :param curr_order:
        """
        opposite_tree = self.bids if not curr_order.is_bid else self.asks
        # we are assuming thar order can not be modified or canceled
        # Try first to match this order with the opposite tree
        trades = opposite_tree.match_price_order(curr_order)
        # If there is remaining order size add it to the matching tree
        if curr_order.peak_size is not 0:
            curr_order.restore_peak_size()
            matching_tree = self.bids if curr_order.is_bid else self.asks
            matching_tree.insert_price_order(curr_order)
        # First print all trades
        for order in trades:
            order.print_trade_result(curr_order.id)
        curr_order.trade_size = 0
        # And then the LOB state
        self.print_book()
        return trades

    def print_book(self):
        print("+-----------------------------------------------------------------+")
        print("| BUY                            | SELL                           |")
        print("| Id       | Volume      | Price | Price | Volume      | Id       |")
        print("+----------+-------------+-------+-------+-------------+----------+")
        bids_it = ComplexIterator(self.bids.tree.values(reverse=True))
        asks_it = ComplexIterator(self.asks.tree.values())
        while bids_it.hasnext() and asks_it.hasnext():
            sys.stdout.write("|")
            next(bids_it).to_print()
            sys.stdout.write("|")
            next(asks_it).to_print()
            sys.stdout.write("|\n")

        while asks_it.hasnext():
            sys.stdout.write("|                                |")
            next(asks_it).to_print()
            sys.stdout.write("|\n")

        while bids_it.hasnext():
            sys.stdout.write("|")
            next(bids_it).to_print()
            sys.stdout.write("|                                |\n")

        print("+-----------------------------------------------------------------+")