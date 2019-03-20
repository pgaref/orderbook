class ComplexIterator(object):
    """
    Returns a linear Value Iterator of a complex data-structure (Tree + DList)
    We iterate through each TreeNode-ListNode  before going to next TreeNode
    """

    def __init__(self, it):
        self.tree_it = iter(it)
        self.order_it = None
        self._next_tree_node = None
        # Values need to be Orders
        self._next_order_value = None
        self._hasnext = None

    def __iter__(self):
        return self

    def next(self):
        # Use latest order value (by hasNext)
        if self._hasnext:
            result = self._next_order_value
        else:
            result = next(self.order_it)
        self._hasnext = None
        return result

    def hasnext(self):
        if self._hasnext is None:
            try:
                # First time called -> tree_node is None go to next
                if self._next_tree_node is None:
                    self._next_tree_node = next(self.tree_it)
                    self.order_it = iter(self._next_tree_node)
                # Next value is the next Order
                self._next_order_value = next(self.order_it)
            except StopIteration:
                try:
                    # We reached end at previous Node so move to next TreeNode
                    self._next_tree_node = next(self.tree_it)
                    self.order_it = iter(self._next_tree_node)
                    self._next_order_value = next(self.order_it)
                except StopIteration:
                    self._hasnext = False
                else:
                    self._hasnext = True
            else:
                self._hasnext = True
        return self._hasnext
