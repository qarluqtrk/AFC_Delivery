import tracemalloc

from sqlalchemy import create_engine, Column, Integer, String, Text, BigInteger
from sqlalchemy.dialects.postgresql import BYTEA
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

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    product_id = Column(Integer)
    quantity = Column(Integer)

    def add_to_cart(self, user_id, product_id, quantity):
        new_cart = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(new_cart)
        session.commit()

    def check(self, user_id, product_id=None):
        if product_id is None:
            if session.query(Cart).filter(Cart.user_id == user_id).all():
                return True
            else:
                return False
        else:
            if session.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first():
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
        for cart_item in cart_items:
            product = PosterAPI(POSTER_API).get_product(cart_item.product_id)
            price = f"{product['spots'][0]['price']}"
            cart_total_price += int(price) * int(cart_item.quantity)

        return str(cart_total_price)


Base.metadata.create_all(engine)
