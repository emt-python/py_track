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
session.add_all(users)
session.commit()

# Insert products
products = [Product(name=f'Product_{i}', price=random.uniform(
    100, 5000)) for i in range(10000)]
session.bulk_save_objects(products)
session.commit()


start_assigning = time.time()

users_from_db = session.query(User).all()
products = session.query(Product).all()

orders = []
for _ in range(2000000):
    order = Order(
        user=random.choice(users_from_db),  # Use users from the database
        product=random.choice(products),    # Assuming products is populated correctly
        quantity=random.randint(1, 10)
    )
    orders.append(order)

session.add_all(orders)
session.commit()

assign_time = time.time() - start_assigning
# print(f"Assign time: {assign_time:.2f} seconds")



# Assuming users_from_db is already populated
users_from_db = session.query(User).all()
print("start deleting")

start_deleting = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
deleted_orders = []

# Loop through a set of random users or all users to process multiple queries
for random_user in random.sample(users_from_db, 40):  # Select 10 random users, or replace with `users_from_db` to process all users
    # print(f"Processing orders for user: {random_user.name}")

    # Query orders associated with the current random user
    orders_to_delete = session.query(Order).filter(Order.user == random_user).all()
    
    for order in orders_to_delete:
        # Fetch the associated product (if necessary)
        product = session.query(Product).filter(Product.id == order.product_id).first()
        
        # Delete the order
        session.delete(order)
        deleted_orders.append(order)
        
        # Flush every 500 deletions to avoid keeping too much data in memory
        if len(deleted_orders) >= 500:
            session.flush()  # Send the changes to the database
            deleted_orders.clear()  # Clear the list to free up memory
    
    # Optional: Flush the remaining orders for this user
    session.flush()
    deleted_orders.clear()

# Commit all the changes after processing all users
session.commit()

if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
delete_time = time.time() - start_deleting
print(f"Delete time: {delete_time:.2f} seconds")
os.remove("user1.db")
