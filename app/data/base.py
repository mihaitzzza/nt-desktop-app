# from time import sleep
from itertools import groupby
from handlers.database import get_session
from models import User, Pizza, Order, OrderedPizza
from utils.constants import SHIPPING_ADDRESS, BILLING_ADDRESS


def get_db_pizza(callback=None):
    # sleep(1)

    session = get_session()
    pizza = session.query(Pizza).all()

    if callback:
        callback(pizza)


def create_order(pizza_list, order_price):
    print('pizza_list', pizza_list)
    # [(1, 2), (2, 2), (4, 1)]
    grouped_data = [(pizza_id, len(list(pizza_group))) for pizza_id, pizza_group in groupby(pizza_list)]

    session = get_session()

    try:
        auth_user = session.query(User).first()
        shipping_address = [address.street for address in auth_user.addresses if address.type.value == SHIPPING_ADDRESS][0]
        billing_address = [address.street for address in auth_user.addresses if address.type.value == BILLING_ADDRESS][0]

        order = Order(user=auth_user, shipping_address=shipping_address, billing_address=billing_address, price=order_price)

        for pizza_id, pizza_quantity in grouped_data:
            ordered_pizza = OrderedPizza(order=order, pizza_id=pizza_id, quantity=pizza_quantity)
            session.add(ordered_pizza)

        session.add(order)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
