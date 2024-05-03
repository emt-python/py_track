import gc
import sys
import time
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import random
from faker import Faker
PYPPER_BIN = "/home/lyuze/workspace/cpython/python"

Base = declarative_base()
fake = Faker()

# Many-to-many relationship table
author_book = Table('author_book', Base.metadata,
                    Column('author_id', Integer, ForeignKey(
                        'authors.id'), primary_key=True),
                    Column('book_id', Integer, ForeignKey(
                        'books.id'), primary_key=True)
                    )


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship('Book', secondary=author_book,
                         back_populates='authors')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    publisher = relationship('Publisher', back_populates='books')
    authors = relationship(
        'Author', secondary=author_book, back_populates='books')


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship('Book', back_populates='publisher')


engine = create_engine('sqlite:///complex_database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
gc.disable()
start_adding = time.time()
# Create Publishers
for _ in range(50000):
    publisher = Publisher(name=fake.company())
    session.add(publisher)
session.commit()
# Create Authors
for _ in range(50000):
    author = Author(name=fake.name())
    session.add(author)
session.commit()
add_time = time.time() - start_adding
print(f"Creating data time: {add_time:.2f} seconds", file=sys.stderr)

# Create Books and randomly assign authors and a publisher to each
# sys.setswitchinterval(0.0001)
start_assigning = time.time()
publishers = session.query(Publisher).all()
authors = session.query(Author).all()
for _ in range(80000):
    book = Book(
        title=fake.sentence(nb_words=4),
        publisher=random.choice(publishers),
        authors=random.sample(authors, k=random.randint(1, 100))
    )
    session.add(book)
session.commit()
assign_time = time.time() - start_assigning
print(f"Assign time: {assign_time:.2f} seconds", file=sys.stderr)


# start_query = time.time()
# query = session.query(
#     Publisher.name,
#     func.count(author_book.c.author_id).label('unique_authors')
# ).join(
#     Book, Publisher.id == Book.publisher_id
# ).join(
#     author_book, Book.id == author_book.c.book_id
# ).group_by(
#     Publisher.id
# ).order_by(
#     func.count(author_book.c.author_id).desc()
# )

# query_time = time.time() - start_query
# print(f"Query time: {query_time:.2f} seconds", file=sys.stderr)

# for name, count in query:
#     print(f"Publisher: {name}, Unique Authors: {count}")
