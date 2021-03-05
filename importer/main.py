import os
import json
from handlers.database import get_session
from models import User, Role, Address, Ingredient, Pizza, Recipe


if __name__ == '__main__':
    with open(os.path.join('data', 'users.json')) as users_file, open(os.path.join('data', 'pizza.json')) as pizza_file:
        users = json.load(users_file)
        pizza = json.load(pizza_file)

    # Get DB session
    session = get_session()

    try:
        # Create users
        for user in users:
            db_user = User(
                first_name=user['first_name'],
                last_name=user['last_name'],
                email=user['email']
            )

            # Create roles if they don't exist and append them to user.
            for user_role in user['roles']:
                db_role = session.query(Role).filter(Role.name == user_role['name']).first()

                if not db_role:
                    db_role = Role(name=user_role['name'])
                    session.add(db_role)

                db_user.roles.append(db_role)

            # Create addresses and append them to user.
            for address in user['addresses']:
                db_address = Address(
                    user=db_user,
                    street=address['street'],
                    city=address['city'],
                    country=address['country'],
                    type=address['type']
                )
                session.add(db_address)

            session.add(db_user)

        # Create pizza
        for pizza_item in pizza:
            pizza_price = 0
            db_pizza = Pizza(name=pizza_item['name'], price=pizza_price)

            for ingredient in pizza_item['ingredients']:
                db_ingredient = session.query(Ingredient).filter(Ingredient.name == ingredient['name']).first()

                if not db_ingredient:
                    db_ingredient = Ingredient(name=ingredient['name'], price=ingredient['price'])
                    session.add(db_ingredient)

                pizza_ingredient = Recipe(pizza=db_pizza, ingredient=db_ingredient, quantity=ingredient['quantity'])
                session.add(pizza_ingredient)
                pizza_price += db_ingredient.price * ingredient['quantity']

            db_pizza.price = pizza_price
            session.add(db_pizza)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
