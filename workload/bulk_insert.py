from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import time
import os, sys
from faker import Faker
is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

enable_tracing = False
if len(sys.argv) != 1:
    print("enable tracing")
    enable_tracing = True

fake = Faker()
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(Text)  # Use Text to hold large strings
    additional_info = Column(Text)  # Another large text field
    image = Column(LargeBinary)  # Simulate storing large binary data

def setup_database(dburl, echo):
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine

def test_bulk_insert(engine, n, batch_size):
    session = Session(bind=engine)
    start_time = time.time()
    customers = []
    for i in range(n):
        customers.append(Customer(
            name=f"Customer {i}",
            description=fake.text(max_nb_chars=5000),  # Enormous text
            additional_info=fake.text(max_nb_chars=5000),  # Enormous text
            image=os.urandom(10 * 512 * 512)  # 1 MB of binary data
        ))
        if len(customers) == batch_size:
            session.bulk_save_objects(customers)
            session.commit()
            customers = []  # Clear the list after commit
    if customers:  # Insert any remaining customers
        session.bulk_save_objects(customers)
        session.commit()
    elapsed_time = time.time() - start_time
    print(f"Inserted {n} customers with very large data.")
    return elapsed_time

def main():
    db_url = 'sqlite://'
    echo = False
    num_rows = 4000  # Number of rows to insert
    batch_size = 50  # Increase batch size for efficiency

    engine = setup_database(db_url, echo)
    if is_pypper and enable_tracing:
        gc_count_module.start_count_gc_list(
            250_000, "obj_dump.txt", 0, 7, 2_500_000)
    elapsed_insertion_time = test_bulk_insert(engine, num_rows, batch_size)  # Bulk insert large data
    if is_pypper and enable_tracing:
        gc_count_module.close_count_gc_list()
    print(f"Compute time: {elapsed_insertion_time:.2f} seconds")

if __name__ == "__main__":
    main()
