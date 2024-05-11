from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, Identity, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import datetime
import os
import time  # Import time for timing executions
import sys
is_pypper = False
if sys.executable == os.path.expanduser("~/workspace/cpython/python"):
    print("is pypper")
    import gc_count_module
    is_pypper = True

enable_tracing = False
if len(sys.argv) != 1:
    print("enable tracing")
    enable_tracing = True

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(Text)  # Text type for large strings
    additional_info = Column(Text)  # Another Text field for large text
    image = Column(LargeBinary)  # Large binary data field

def setup_database(dburl, echo):
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine

def populate_data(engine, num_records):
    session = Session(bind=engine)
    start_populate = time.time()  # Start timing for data population
    for i in range(num_records):
        # Generate large amounts of data
        name = "Customer " + str(i)
        description = " ".join(["A lot of details"] * 500)  # Very large text
        additional_info = " ".join(["Additional info"] * 500)  # Very large text
        image_data = os.urandom(5 * 1024 * 1024)  # 10 MB of binary data
        customer = Customer(name=name, description=description, additional_info=additional_info, image=image_data)
        session.add(customer)
    session.commit()
    end_populate = time.time()  # End timing for data population
    print(f"Time to populate {num_records} customers: {end_populate - start_populate:.2f} seconds")

def query_data(engine):
    session = Session(bind=engine)
    start_query = time.time()  # Start timing for query
    result = session.execute(select(Customer)).fetchall()
    end_query = time.time()  # End timing for query
    print(f"Fetched {len(result)} customers")
    print(f"Query time: {end_query - start_query:.2f} seconds")
    session.close()

def main():
    db_url = 'sqlite://'
    echo = False
    num_rows = 1200  # Number of records to insert
    engine = setup_database(db_url, echo)
    
    populate_data(engine, num_rows)
    start_time = time.time()  # Start overall timing
    if is_pypper and enable_tracing:
        gc_count_module.start_count_gc_list(
            250_000, "obj_dump.txt", 0, 7, 2_500_000)
    query_data(engine)
    if is_pypper and enable_tracing:
        gc_count_module.close_count_gc_list()
    end_time = time.time()  # End overall timing
    
    print(f"Compute time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
