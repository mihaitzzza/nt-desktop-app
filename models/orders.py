from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DOUBLE
from models import Base, CustomModel, User, Pizza


class Order(Base, CustomModel):
    __tablename__ = 'orders'
    user_id = Column(INTEGER, ForeignKey(User.id))
    user = relationship(User, backref='orders')
    shipping_address = Column(VARCHAR(255), nullable=False)
    billing_address = Column(VARCHAR(255), nullable=False)
    price = Column(DOUBLE, nullable=False, default=0.00)
    pizza = relationship(Pizza, secondary='order_pizza')


class OrderedPizza(Base, CustomModel):
    __tablename__ = 'order_pizza'
    __table_args__ = (UniqueConstraint('order_id', 'pizza_id'),)

    order_id = Column(INTEGER, ForeignKey(Order.id))
    order = relationship(Order, backref=backref('order_pizza', cascade='all, delete-orphan'))

    pizza_id = Column(INTEGER, ForeignKey(Pizza.id))
    pizza = relationship(Pizza, backref=backref('order_pizza', cascade='all, delete-orphan'))

    quantity = Column(INTEGER, nullable=False, default=1)
