class OrderList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
        self._temp = None 

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
        if self.head is not None:
            order.prev_order = self.tail
            order.next_order = None
            self.tail.next_order = order
            self.tail = order
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
        if self.size == 0:
            self.head = None
            self.tail = None
        tmp_next = order.next_order
        tmp_prev = order.prev_order
        if tmp_next is not None and tmp_prev is not None:
            tmp_next.prev_order = tmp_prev
            tmp_prev.next_order = tmp_next
        elif tmp_next is not None:
            tmp_next.prev_order = None
            self.head = tmp_next
        elif tmp_prev is not None:
            tmp_prev.next_order = None
            self.tail = tmp_prev

    def match_order(self, other_order, order_map):
        complete_orders = []
        current_order = self.head
        while other_order.peak_size > 0 and self.size > 0:
            fully_matched = current_order.match(other_order)
            if fully_matched:
                current_next = current_order.next_order
                if current_order.peak_size == 0:
                    complete_orders.append(current_order)
                    del order_map[current_order.id]
                    self.remove(current_order)
                current_order = current_next
                if current_next is None:
                    current_order = self.head

        for order in iter(self):
            if order.trade_size > 0:
                complete_orders.append(order)
        return complete_orders

    def __iter__(self):
        self._temp = self.head
        return self

    def next(self):
        if self._temp is None:
            raise StopIteration
        else:
            return_val = self._temp
            self._temp = self._temp.next_order
            return return_val

    __next__ = next  
