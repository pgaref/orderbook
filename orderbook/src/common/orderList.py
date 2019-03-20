class OrderList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
        self._temp = None  # Temp iterator variable

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, new_head):
        self._head = new_head

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, new_tail):
        self._tail = new_tail

    @property
    def size(self):
        return self._size

    def add(self, order):
        """
        Add to tail
        :param order:
        :return:
        """
        #  Non-empty list
        if self.head is not None:
            order.prev_order = self.tail
            order.next_order = None
            self.tail.next_order = order
            self.tail = order
        #  First element
        else:
            order.next_order = None
            order.prev_order = None
            self.head = order
            self.tail = order
        self._size += 1

    def remove_head(self):
        self.remove(self.head)

    def remove_tail(self):
        self.remove(self.tail)

    def remove(self, order):
        """
        We assume that the given element is always part of the List
        :param order:
        :return:
        """
        self._size -= 1
        # Removing last element of the List
        if self.size == 0:
            self.head = None
            self.tail = None
        # Remove from list of orders
        tmp_next = order.next_order
        tmp_prev = order.prev_order
        # Removing intermediate
        if tmp_next is not None and tmp_prev is not None:
            tmp_next.prev_order = tmp_prev
            tmp_prev.next_order = tmp_next
        # Removing head
        elif tmp_next is not None:
            tmp_next.prev_order = None
            self.head = tmp_next
        # Removing tail
        elif tmp_prev is not None:
            tmp_prev.next_order = None
            self.tail = tmp_prev

    def match_order(self, other_order, order_map):
        """
         Match with orders in list method ensuring precedence (older orders fist)
         Start from head (we add to tail) and also loop when needed
         Any different match strategy should override this method
        :param other_order:
        :param order_map:
        """
        # no match cases
        # if other_order.is_bid and other_order.price < self.head.price:
        #     return
        # if not other_order.is_bid and other_order.price > self.head.price:
        #     return

        complete_orders = []
        # Iterate orders and make trades
        current_order = self.head
        # We loop until either the whole price-tree is gone or we run out of peak-size!
        while other_order.peak_size > 0 and self.size > 0:
            fully_matched = current_order.match(other_order)
            # When fully matched go to next order (assume that Icebergs will have to wait their turn)
            if fully_matched:
                current_next = current_order.next_order
                # When current_order is exhausted add to complete list
                if current_order.peak_size == 0:
                    complete_orders.append(current_order)
                    del order_map[current_order.id]
                    self.remove(current_order)
                current_order = current_next
                # reached the end of the list start-over!!
                if current_next is None:
                    current_order = self.head

        for order in iter(self):
            if order.trade_size > 0:
                complete_orders.append(order)
        return complete_orders

    # Custom iterator functionality
    def __iter__(self):
        # Always start from head
        self._temp = self.head
        return self

    def next(self):
        # When next is called on an empty temp (iteration is over)
        if self._temp is None:
            raise StopIteration
        # Return next list element (temp.next)
        else:
            return_val = self._temp
            self._temp = self._temp.next_order
            return return_val

    __next__ = next  # Python 3.x compatibility
