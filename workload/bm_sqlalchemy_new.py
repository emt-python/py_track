import os
import time
from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random
from faker import Faker
import sys
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

Base = declarative_base()
fake = Faker()

# Remove old database file if exists
if os.path.exists("hospitality_complex.db"):
    os.remove("hospitality_complex.db")

# Many-to-many relationship table for waiters and tables
waiter_table = Table('waiter_table', Base.metadata,
                     Column('waiter_id', Integer, ForeignKey(
                         'waiters.id'), primary_key=True),
                     Column('table_id', Integer, ForeignKey('tables.id'), primary_key=True))


class Waiter(Base):
    __tablename__ = 'waiters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    biography = Column(Text)  # Adding a large text field
    image = Column(LargeBinary)  # New binary data field
    tables = relationship('Table', secondary=waiter_table,
                          back_populates='waiters')


class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    description = Column(Text)  # Adding a large text field
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates='tables')
    waiters = relationship(
        'Waiter', secondary=waiter_table, back_populates='tables')


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)  # Adding a large text field
    image = Column(LargeBinary)  # New binary data field
    tables = relationship('Table', back_populates='restaurant')


engine = create_engine('sqlite:///hospitality_complex.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create restaurants with larger data footprint
start_adding = time.time()
restaurants = [Restaurant(name=fake.company(), description=fake.paragraph(
    nb_sentences=50), image=os.urandom(1*1024*1024)) for _ in range(2000)]
session.add_all(restaurants)
session.commit()

# Create waiters with larger data footprint
waiters = [Waiter(name=fake.name(), biography=fake.paragraph(
    nb_sentences=100), image=os.urandom(1*1024*1024)) for _ in range(2000)]
session.add_all(waiters)
session.commit()
add_time = time.time() - start_adding
print(f"Creating data time: {add_time:.2f} seconds")

# Assign tables to restaurants and waiters with more complexity
start_assigning = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 1024, 1_000_000, 5)
for _ in range(50000):
    table = Table(
        number=fake.building_number(),
        description=fake.paragraph(nb_sentences=20),
        restaurant=random.choice(restaurants),
        # Increase complexity
        waiters=random.sample(waiters, k=random.randint(1, 20))
    )
    session.add(table)
session.commit()
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
assign_time = time.time() - start_assigning
print(f"Compute time: {assign_time:.2f} seconds")

print("Database populated with an extremely large footprint.")
os.remove("hospitality_complex.db")
