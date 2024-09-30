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
if os.path.exists("complex_database.db"):
    print("delete old db", file=sys.stderr)
    os.remove("user3.db")
# Setup
Base = declarative_base()
engine = create_engine('sqlite:///user3.db')
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


# Fetch a random user
random_user = random.choice(session.query(User).all())

# Fetch all orders for the random user
orders_to_delete = session.query(Order).filter(Order.user == random_user).all()

# Keep track of the orders being deleted without committing in small batches
deleted_orders = []

# Delete orders in batches
for order in orders_to_delete:
    # Simulate a memory-intensive operation (fetch related product data)
    product = session.query(Product).filter(
        Product.id == order.product_id).first()

    # Perform the deletion
    session.delete(order)

    # Add to the deleted batch list
    deleted_orders.append(order)

    # Flush in batches of 5000 but don't commit yet
    if len(deleted_orders) % 5000 == 0:
        print(f"Processing batch of {len(deleted_orders)} deletions")
        session.flush()  # Flush without committing to increase memory pressure
        deleted_orders.clear()  # Clear the list to free memory for the next batch

# Commit after all deletions
session.commit()

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
assign_time = time.time() - start_assigning
print(f"Assign time: {assign_time:.2f} seconds")
os.remove("user3.db")
