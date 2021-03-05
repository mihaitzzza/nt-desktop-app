import enum
from sqlalchemy import Column, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.orm import relationship, backref
from utils.constants import SHIPPING_ADDRESS, BILLING_ADDRESS
from models import Base, CustomModel


class User(Base, CustomModel):
    __tablename__ = 'users'
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    roles = relationship('Role', secondary='user_roles')


class Role(Base, CustomModel):
    __tablename__ = 'roles'
    name = Column(VARCHAR(255), nullable=False, unique=True)
    users = relationship('User', secondary='user_roles')


class UserRole(Base, CustomModel):
    __tablename__ = 'user_roles'
    __table_args__ = (UniqueConstraint('user_id', 'role_id'),)

    user_id = Column(INTEGER, ForeignKey(User.id))
    user = relationship(User, backref=backref('user_roles', cascade='all, delete-orphan'))

    role_id = Column(INTEGER, ForeignKey(Role.id))
    role = relationship(Role, backref=backref('user_roles', cascade='all, delete-orphan'))


class Address(Base, CustomModel):
    __tablename__ = 'addresses'
    __table_args__ = (UniqueConstraint('user_id', 'type'),)

    user_id = Column(INTEGER, ForeignKey(User.id))
    user = relationship(User, backref='addresses')

    # The following Enum is used in setting the `addresses.type` field.
    # This can have only the value of SHIPPING or BILLING.
    class Types(enum.Enum):
        SHIPPING = SHIPPING_ADDRESS
        BILLING = BILLING_ADDRESS
    type = Column(Enum(Types))

    street = Column(VARCHAR(255), nullable=False)
    city = Column(VARCHAR(255), nullable=False)
    country = Column(VARCHAR(255), nullable=False)
