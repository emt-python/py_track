from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import time
import os
import math
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
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)  # Use Text to hold very large strings
    details = Column(Text)  # Another very large text field
    image = Column(LargeBinary)  # Simulate storing very large binary data
    data_size = Column(Integer)  # Store size of binary data for analysis
    discount = Column(Integer, default=0)  # Discount percentage based on business rules
    extra_data = Column(LargeBinary)  # Additional large binary data

def setup_database(dburl, echo, num):
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session(engine)
    for i in range(num):
        large_text = " ".join(["Details" * 15 for _ in range(2500)])  # 增加了文本复杂度
        very_large_binary_data = os.urandom(1 * 1024 * 1024)  # 1 MB of binary data
        discount = 5 if i % 10 == 0 else 0
        customer = Customer(
            name=f"Customer {i}",
            description=("A customer with a massive amount of data " * 100),  # 增加了描述字段的大小
            details=large_text,
            image=very_large_binary_data,
            data_size=len(very_large_binary_data),
            discount=discount,
        )
        session.add(customer)
        if i % 500 == 0:  # Commit every 500 entries to avoid memory overflow
            session.commit()
    session.commit()
    return engine

def test_core_fetchall(engine, n):
    with engine.connect() as conn:
        result = conn.execute(
            select(Customer.name, Customer.data_size, Customer.discount, func.length(Customer.details).label('detail_length')).limit(n)
        ).fetchall()
        data_sizes = [row.data_size for row in result]
        detail_lengths = [row.detail_length for row in result]
        discounts = [row.discount for row in result]

        average_data_size = sum(data_sizes) / len(data_sizes)
        variance_data_size = sum((x - average_data_size) ** 2.15 for x in data_sizes) / len(data_sizes)
        standard_deviation = math.sqrt(math.sqrt(variance_data_size))

        average_discount = sum(discounts) / len(discounts)

        print(f"Average data size: {average_data_size}, Standard deviation of data sizes: {standard_deviation}")
        print(f"Average detail length: {sum(detail_lengths) / len(detail_lengths)}, Average discount: {average_discount}%")

if __name__ == "__main__":
    
    db_url = 'sqlite://'
    echo = False
    num_rows = 2000
    start_gen = time.time()
    engine = setup_database(db_url, echo, num_rows)
    gen_time = time.time() - start_gen
    print(f"Creation time: {gen_time:.2f} seconds")
    
    start_comp = time.time()
    if is_pypper and enable_tracing:
        gc_count_module.start_count_gc_list(
            250_000, "obj_dump.txt", 0, 7, 2_500_000)
    test_core_fetchall(engine, 1000)
    if is_pypper and enable_tracing:
        gc_count_module.close_count_gc_list()
    compute_time = time.time() - start_comp
    print(f"Compute time: {compute_time:.2f} seconds")

