import pyperf

from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import insert

from faker import Faker
fake = Faker()
metadata = MetaData()

Person = Table('person', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(250), nullable=False))

Address = Table('address', metadata,
                Column('id', Integer, primary_key=True),
                Column('street_name', String(250)),
                Column('street_number', String(250)),
                Column('post_code', String(250), nullable=False),
                Column('person_id', Integer, ForeignKey('person.id')))

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///imperative.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
metadata.create_all(engine)


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# add 'npeople' people to the database


def bench_sqlalchemy(loops, npeople):
    total_dt = 0.0
    with engine.connect() as connection:
        for loops in range(loops):
            # drop rows created by the previous benchmark
            cur = Person.delete()
            connection.execute(cur)

            cur = Address.delete()
            connection.execute(cur)

            # Run the benchmark once
            t0 = pyperf.perf_counter()

            for i in range(npeople):
                # Insert a Person in the person table
                insert_statement = insert(Person).values(name=fake.name())
                connection.execute(insert_statement)

                # Insert an Address in the address table
                new_address = insert(Address).values(post_code=fake.name())
                connection.execute(new_address)

            # do 'npeople' queries per insert
            for i in range(npeople):
                cur = Person.select()
                connection.execute(cur)

            total_dt += (pyperf.perf_counter() - t0)

    return total_dt


if __name__ == "__main__":
    bench_sqlalchemy(1, 999999)
