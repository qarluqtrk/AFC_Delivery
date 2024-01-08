import tracemalloc

from sqlalchemy import create_engine, Column, Integer, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base

from data.config import POSTER_API
from utils.poster_api.AFC import PosterAPI

tracemalloc.start()

db_url = "postgresql+psycopg2://postgres:22@localhost:5432/afcbot"
engine = create_engine(url=db_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Cart(Base):
    __tablename__ = "cart"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    product_id = Column(Integer)
    modificator_id = Column(Integer, nullable=True)
    quantity = Column(Integer)

    def add_to_cart(self, user_id, product_id, quantity):
        new_cart = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(new_cart)
        session.commit()

    def add_to_cart_modificator(self, user_id, product_id, modificator_id, quantity):
        new_cart = Cart(user_id=user_id, product_id=product_id, modificator_id=modificator_id, quantity=quantity)
        session.add(new_cart)
        session.commit()

    def check(self, user_id, product_id=None, modificator_id=None):
        if product_id is None:
            if session.query(Cart).filter(Cart.user_id == user_id).all():
                return True
            else:
                return False
        else:
            if modificator_id is None:
                if session.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first():
                    return True
                else:
                    return False
            else:
                if session.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id,
                                              Cart.modificator_id == modificator_id).first():
                    return True
                else:
                    return False

    def get_cart(self, user_id):
        return session.query(Cart).filter(Cart.user_id == user_id).order_by(Cart.id).all()

    def clear(self, user_id):
        session.query(Cart).filter(Cart.user_id == user_id).delete()
        session.commit()

    def cart_total(self, user_id):
        cart_items = session.query(Cart).filter(Cart.user_id == user_id).order_by(Cart.id).all()
        cart_total_price = 0
        price = ''
        products = {}
        products_poster = PosterAPI(POSTER_API).get_products()
        for i in products_poster:
            products[(i['product_id'])] = i
        for cart_item in cart_items:
            product = products[f"{cart_item.product_id}"]
            if cart_item.modificator_id is None:
                price = f"{product['sources'][1]['price']}"
            else:
                if 'modifications' in product:
                    for modification in product['modifications']:
                        if modification['modificator_id'] == str(cart_item.modificator_id):
                            price = f"{modification['sources'][1]['price']}"
                            break
                elif 'group_modifications' in product:
                    for modification in product['group_modifications'][0]['modifications']:
                        if modification['dish_modification_id'] == int(cart_item.modificator_id):
                            price = f"{modification['price']}" + '00'
                            price = int(price)
                            break
            cart_total_price += int(price) * int(cart_item.quantity)

        return str(cart_total_price)


Base.metadata.create_all(engine)
