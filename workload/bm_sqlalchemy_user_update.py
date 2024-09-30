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
    os.remove("user2.db")
# Setup
Base = declarative_base()
engine = create_engine('sqlite:///user2.db')
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

# Fetch all orders from the database
orders = session.query(Order).all()

# Keep track of updates without committing in small batches
updated_orders = []
large_list = []  # Additional large in-memory data structure

# Update quantities and potentially other fields of all orders
for order in orders:
    # Update quantity to a random value between 1 and 100
    order.quantity = random.randint(100, 10000)

    # Update product price
    order.product.price = random.uniform(500, 20000)

    # Simulate memory-intensive operations
    # Example 1: Add large in-memory operations by creating random strings
    order.product.name = ''.join(random.choices(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10000))

    # Example 2: Complex calculations
    for _ in range(1000):  # Large inner loop for calculation
        value = random.random() ** 2

    # Example 3: Build a large in-memory data structure
    large_list.append({
        'order_id': order.id,
        'user_name': order.user.name,
        'product_name': order.product.name
    })

    # Append to batch for update
    updated_orders.append(order)

    # Introduce a memory-intensive operation by delaying the commit until the batch is large
    if len(updated_orders) % 5000 == 0:
        print(f"Processing batch of {len(updated_orders)} orders")
        session.bulk_save_objects(updated_orders)
        session.flush()  # Flush but do not commit yet to increase memory pressure
        updated_orders.clear()  # Clear the list to free memory for the next batch

# Commit after all updates
session.commit()
# Optional: Clear the large in-memory data structure
large_list.clear()


if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
assign_time = time.time() - start_assigning
print(f"Assign time: {assign_time:.2f} seconds")
os.remove("user2.db")
