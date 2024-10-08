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
    100, 5000)) for i in range(10000)]
session.bulk_save_objects(products)
session.commit()


start_assigning = time.time()

users = session.query(User).all()
products = session.query(Product).all()

orders = []
for _ in range(4000000):
    order = Order(
        user=random.choice(users),
        product=random.choice(products),
        quantity=random.randint(1, 10)
    )
    orders.append(order)

session.bulk_save_objects(orders)
session.commit()

assign_time = time.time() - start_assigning
# print(f"Assign time: {assign_time:.2f} seconds")


orders = session.query(Order).all()
subset_size = int(len(orders) * 0.03)
random_orders = random.sample(orders, subset_size)
print(len(random_orders))
start_updating = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
updated_orders = []
large_list = []
# Iterate over the randomly selected 25% of orders
for order in random_orders:
    # for order in orders:
    order.quantity = random.randint(1000, 100000)
    if order.product is None:
        order.product = random.choice(products)
    order.product.price = random.uniform(5000, 20000)
    # for _ in range(1000):  # Large inner loop for calculation
    #     value = random.random() ** 2
    if order.user is None:
        order.user = random.choice(users)

    # Example 3: Build a large in-memory data structure
    large_list.append({
        'order_id': order.id,
        'user_name': order.user.name,
        'product_name': order.product.name
    })

    # Append to batch for update
    updated_orders.append(order)

    # Introduce a memory-intensive operation by delaying the commit until the batch is large
    # if len(updated_orders) % 5 == 0:
    # print(f"Processing batch of {len(updated_orders)} orders")
    session.bulk_save_objects(updated_orders)
    session.flush()  # Flush but do not commit yet to increase memory pressure
    updated_orders.clear()  # Clear the list to free memory for the next batch

session.commit()

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
update_time = time.time() - start_updating
print(f"Update time: {update_time:.2f} seconds")
large_list.clear()
os.remove("user1.db")
