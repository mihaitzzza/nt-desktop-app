from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DOUBLE
from models import Base, CustomModel


class Ingredient(Base, CustomModel):
    __tablename__ = 'ingredients'
    name = Column(VARCHAR(255), nullable=False, unique=True)
    price = Column(DOUBLE, nullable=False, default=0.00)
    stock = Column(INTEGER, nullable=False, default=0)
    pizza_types = relationship('Pizza', secondary='pizza_ingredients')


class Pizza(Base, CustomModel):
    __tablename__ = 'pizza'
    name = Column(VARCHAR(255), nullable=False, unique=True)
    price = Column(DOUBLE, nullable=False, default=0.00)
    ingredients = relationship('Ingredient', secondary='pizza_ingredients')
    orders = relationship('Order', secondary='order_pizza')


class Recipe(Base, CustomModel):
    __tablename__ = 'pizza_ingredients'
    __table_args__ = (UniqueConstraint('pizza_id', 'ingredient_id'),)

    pizza_id = Column(INTEGER, ForeignKey(Pizza.id))
    pizza = relationship(Pizza, backref=backref('pizza_ingredients', cascade='all, delete-orphan'))

    ingredient_id = Column(INTEGER, ForeignKey(Ingredient.id))
    ingredient = relationship(Ingredient, backref=backref('pizza_ingredients', cascade='all, delete-orphan'))

    quantity = Column(INTEGER, nullable=False, default=1)
