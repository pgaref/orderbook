# Wrapper method to satisfy setup.py entry_point
import sys

from orderbook.src.common.order import Order
from orderbook.src.orderBook import OrderBook
from timeit import default_timer as timer


def main():
    book = OrderBook()
    start = timer()
    count = 0
    while True:
        try:
            line = sys.stdin.readline()

            order_fields = line.split(",")
            # Probably reached end of file
            if not line or len(order_fields) < 4 or len(order_fields) > 5:
                sys.stderr.write("Unrecognized message: {0}\n".format(line))
                break
            order_type = order_fields[0]  # 'B' or 'S'
            order_id = order_fields[1]
            order_price = int(order_fields[2])  # in pence > 0
            order_size = int(order_fields[3])  # quantity > 0
            new_order = Order(order_type, order_id, order_price, order_size,
                              int(order_fields[4]) if len(order_fields) == 5 else None)
            book.process_order(new_order)
        except KeyboardInterrupt:
            break
        count += 1
    total = timer() - start
    print("Done processing {0} lines of input".format(count))
    print("Processed {} orders in {:.2f} sec - avg: {} orders/second"
          .format(count, total, int(count/total)))


if __name__ == '__main__':
    main()