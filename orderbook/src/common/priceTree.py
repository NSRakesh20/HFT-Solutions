from bintrees import FastRBTree

from orderbook.src.common.orderList import OrderList


class PriceTree(object):
    def __init__(self, name):
        self.tree = FastRBTree()
        self.name = name
        self.price_map = {}  
        self.order_map = {}  
        self.min_price = None
        self.max_price = None

    def insert_price(self, price):
        """
        Add a new price TreedNode and associate it with an orderList
        :param price:
        :return:
        """
        new_list = OrderList()
        self.tree.insert(price, new_list)
        self.price_map[price] = new_list
        if self.max_price is None or price > self.max_price:
            self.max_price = price
        if self.min_price is None or price < self.min_price:
            self.min_price = price

    def remove_price(self, price):
        self.tree.remove(price)

        for to_del_order in self.price_map[price]:
            del self.order_map[to_del_order.id]
        del self.price_map[price]
        if self.max_price == price:
            try:
                self.max_price = self.tree.max_key()
            except ValueError:
                self.max_price = None
        if self.min_price == price:
            try:
                self.min_price = self.tree.min_key()
            except ValueError:
                self.min_price = None

    def insert_price_order(self, order):
        if order.price not in self.price_map:
            self.insert_price(order.price)
        self.price_map[order.price].add(order)
        self.order_map[order.id] = order

    def match_price_order(self, curr_order):
        if len(self.price_map) == 0:
            return []
        best_price = self.min if curr_order.is_bid else self.max
        complete_trades = []
        while ((curr_order.is_bid and curr_order.price >= best_price)
                or (not curr_order.is_bid and curr_order.price <= best_price)) \
                and curr_order.peak_size > 0:
            # Get price OrderList
            matching_orders_list = self.get_price(best_price)
            complete_trades.extend(matching_orders_list.match_order(curr_order, self.order_map))
            # Remove exhausted price
            if matching_orders_list.size == 0:
                self.remove_price(best_price)
                if len(self.price_map) == 0:
                    break
                # Try to find more price matches using the next price
                best_price = self.min if curr_order.is_bid else self.max

        return complete_trades

    def price_exists(self, price):
        return price in self.price_map

    def order_exists(self, id_num):
        return id_num in self.order_map

    def get_price(self, price):
        return self.price_map[price]

    def get_order(self, id_num):
        return self.order_map[id_num]

    @property
    def max(self):
        return self.max_price

    @property
    def min(self):
        return self.min_price
