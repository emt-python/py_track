from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
import random

from faker import Faker
import sys
import time
import os

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

if sys.argv[1] == "no_gc":
    print("running no gc")
    import gc
    gc.disable()
elif sys.argv[1] == "with_gc":
    print("running with gc")
else:
    print("Using GC or not? Forget to specify?")

enable_tracing = False
if len(sys.argv) != 2:
    print("enable tracing")
    enable_tracing = True

fake = Faker()
if os.path.exists("user1.db"):
    print("delete user1", file=sys.stderr)
    os.remove("user1.db")
# Setup
Base = declarative_base()
engine = create_engine('sqlite:///user1.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define Models


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    user = relationship("User")
    product = relationship("Product")


# Create the tables
Base.metadata.create_all(engine)


# Insert users
users = [User(name=f'User_{i}') for i in range(1000)]
session.bulk_save_objects(users)
session.commit()

# Insert products
products = [Product(name=f'Product_{i}', price=random.uniform(
    1000, 50000)) for i in range(1000000)]
session.bulk_save_objects(products)
session.commit()


start_assigning = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
users = session.query(User).all()
products = session.query(Product).all()

orders = []
for _ in range(5000000):
    order = Order(
        user=random.choice(users),
        product=random.choice(products),
        quantity=random.randint(1, 10)
    )
    orders.append(order)

session.bulk_save_objects(orders)
session.commit()
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
assign_time = time.time() - start_assigning
print(f"Assign time: {assign_time:.2f} seconds")
os.remove("user1.db")
