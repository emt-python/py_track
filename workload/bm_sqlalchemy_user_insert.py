from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
import random

from faker import Faker
import sys
import time
import os
import gc

is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

if sys.argv[1] == "no_gc":
    print("running no gc")
    gc.disable()
elif sys.argv[1] == "with_gc":
    print("running with gc")
else:
    print("Using GC or not? Forget to specify?")

enable_tracing = False
if len(sys.argv) != 2:
    print("enable tracing")
    enable_tracing = True

gc.disable()
Base = declarative_base()
fake = Faker()
if os.path.exists("user1.db"):
    print("delete user1", file=sys.stderr)
    os.remove("user1.db")

# Define the user_product association table
# user_product = Table('user_product', Base.metadata,
#                      Column('user_id', Integer, ForeignKey(
#                          'users.id'), primary_key=True),
#                      Column('product_id', Integer, ForeignKey(
#                          'products.id'), primary_key=True)
#                      )
order_user = Table('order_user', Base.metadata,
                   Column('order_id', Integer, ForeignKey(
                       'orders.id'), primary_key=True),
                   Column('user_id', Integer, ForeignKey(
                       'users.id'), primary_key=True)
                   )


# Define the User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Many-to-many relationship with orders
    orders = relationship('Order', secondary=order_user,
                          back_populates='users')


# Define the Product class
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    orders = relationship('Order', back_populates='product')


# Define the Order class
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    description = Column(String)
    product_id = Column(Integer, ForeignKey('products.id'))
    # Many-to-many relationship with users
    users = relationship('User', secondary=order_user, back_populates='orders')
    product = relationship('Product', back_populates='orders')


# Setup
engine = create_engine('sqlite:///user1.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
start_adding = time.time()
# Insert users
for _ in range(50000):
    user = User(name=fake.company())
    session.add(user)
# users = [User(name=f'User_{i}') for i in range(1000)]
# session.bulk_save_objects(users)
session.commit()

# Insert products
for _ in range(50000):
    product = Product(name=fake.name())
    session.add(product)
# products = [Product(name=f'Product_{i}', price=random.uniform(
#     1000, 50000)) for i in range(1000000)]
# session.bulk_save_objects(products)
session.commit()
add_time = time.time() - start_adding
print(f"Creating data time: {add_time:.2f} seconds", file=sys.stderr)


start_assigning = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)

users = session.query(User).all()
products = session.query(Product).all()

for _ in range(80000):
    order = Order(
        quantity=fake.random_number(digits=3),  # Generate quantity (3 digits)
        product=random.choice(products),
        description=fake.sentence(nb_words=4),
        users=random.sample(users, k=random.randint(1, 100))
    )
    session.add(order)
# orders = []
# for _ in range(5000000):
#     order = Order(
#         user=random.choice(users),
#         product=random.choice(products),
#         quantity=random.randint(1, 10)
#     )
#     orders.append(order)

# session.bulk_save_objects(orders)
session.commit()
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
assign_time = time.time() - start_assigning
print(f"Assign time: {assign_time:.2f} seconds")
os.remove("user1.db")
