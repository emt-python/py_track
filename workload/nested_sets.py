from sqlalchemy import create_engine, Column, Integer, String, select, event, func, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import time
import random
import hashlib
import json
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

class Employee(Base):
    __tablename__ = "personnel"
    emp = Column(String, primary_key=True)
    left = Column("lft", Integer, nullable=False)
    right = Column("rgt", Integer, nullable=False)
    data = Column(String)
    large_text = Column(String)  # Large text field
    complex_data = Column(String)  # JSON data
    binary_data = Column(LargeBinary)  # Simulating large binary data such as images

    def __repr__(self):
        return f"Employee({self.emp}, L:{self.left}, R:{self.right}, Data: {self.data[:30]}...)"

@event.listens_for(Employee, "before_insert")
def before_insert(mapper, connection, instance):
    if not instance.left and not instance.right:  # Assuming it's a root node if no values yet
        instance.left = 1
        instance.right = 2
        instance.data = hashlib.sha256(f"New Employee {random.random()}".encode()).hexdigest()
    else:
        max_right = connection.scalar(select(func.max(Employee.right))) or 0
        instance.left = max_right + 1
        instance.right = max_right + 2

    # Increase complexity of the generated data
    random_data = [random.randint(1, 1000) for _ in range(10000)]  # Reduced array size for balance
    instance.large_text = fake.text(max_nb_chars=100000)  # Slightly larger text
    instance.complex_data = json.dumps({"numbers": random_data})  # Store complex structured data
    instance.binary_data = os.urandom(50 * 1024 * 1024)  # Adjusted binary data size for demonstration

engine = create_engine("sqlite://", echo=False)
Base.metadata.create_all(engine)

session = Session(bind=engine)

# Timing for record creation
start_data_generation_time = time.time()
employees = [
    Employee(emp=f"Employee_{i}") for i in range(100)
]
end_data_generation_time = time.time()
data_generation_time = end_data_generation_time - start_data_generation_time
print(f"Data generation time: {data_generation_time:.2f} seconds")

# Timing for database operation
start_database_time = time.time()
if is_pypper and enable_tracing:
    gc_count_module.start_count_gc_list(
        250_000, "obj_dump.txt", 0, 7, 2_500_000)
session.add_all(employees)
session.commit()
if is_pypper and enable_tracing:
    gc_count_module.close_count_gc_list()
end_database_time = time.time()
database_operation_time = end_database_time - start_database_time
print(f"Compute time: {database_operation_time:.2f} seconds")


session.close()
