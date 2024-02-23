import time
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey, Boolean
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError



class Base(DeclarativeBase):
    pass



class MemberBooks(Base):
    __tablename__ = 'member_book'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    book_id = Column('book_id', String, ForeignKey('books.ISBN_number'))

    def __str__(self) -> str:
        return f'{self.user_id} and {self.id}'


class MemberMagazine(Base):
    __tablename__ = 'member_magazine'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    magazine_id = Column('magazine_id', String,
                         ForeignKey('magazines.ISSN_number'))

    def __str__(self) -> str:
        return f'{self.user_id} and {self.id}'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow().date())
    expiry_date = Column(
        DateTime(), default=datetime.utcnow().date() + timedelta(days=60))
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    fine = Column(Integer,default=0)
    book_id = relationship(
        'Books', secondary='member_book', back_populates='user_id')
    magazine_id = relationship(
        'Magazine', secondary='member_magazine', back_populates='user_id')
    record = relationship('Record', backref='user')

    
    def __str__(self):
        return f'{self.__tablename__}'


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(200))
    phone_number = Column(BigInteger())
    books = relationship('Books', backref='publisher')
    magazine = relationship('Magazine', backref='publisher')


class Books(Base):
    __tablename__ = 'books'
    ISBN_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    book_title = Column(String(100), nullable=False)
    author = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_book', back_populates='book_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='book')


    def __str__(self):
        return f'{self.__tablename__}'


class Magazine(Base):
    __tablename__ = 'magazines'
    ISSN_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    magazine_title = Column(String(100), nullable=False)
    editor = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_magazine', back_populates='magazine_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='magazine')

    def __str__(self):
        return f'{self.__tablename__}'


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer(), primary_key=True)
    genre_name = Column(String(50), nullable=False, default='Lore')
    books = relationship('Books', backref='genre')
    magazine = relationship('Magazine', backref='genre')
    record = relationship('Record', backref='genre')

    def __str__(self):
        return f'{self.__tablename__}'


class Librarian(Base):
    __tablename__ = 'librarians'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())

    def __str__(self):
        return f'{self.__tablename__}'


class Record(Base):
    __tablename__ = 'records'
    record_id = Column(Integer(), primary_key=True)
    member_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(String, ForeignKey('books.ISBN_number'))
    magazine_id = Column(String, ForeignKey('magazines.ISSN_number'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    issued_date = Column(DateTime(), default=datetime.utcnow().date())
    returned_date = Column(DateTime())
    expected_return_date = Column(DateTime(), default=(
        datetime.utcnow().date() + timedelta(days=15)))
    returned = Column(Boolean, default=False)


def create_database(engine, session, dummy_data):
    Base.metadata.create_all(engine)
    if dummy_data:

        genre1 = Genre(genre_name='Educational')
        genre2 = Genre(genre_name='Action')
        genre3 = Genre(genre_name='Folktale')
        publisher1 = Publisher(
            name="ABC Publishers",
            address="Kathmandu",
            phone_number=9810204567
        )

        publisher2 = Publisher(
            name="Test Publishers",
            address="Pokhara",
            phone_number=9810204527
        )

        book1 = Books(ISBN_number='1234567891011', 
                      author='Rohan', 
                      book_title='Very Good Book',
                      price=800, 
                      available_number=50, 
                      publisher=publisher1, 
                      genre=genre1
                      )
        
        book2 = Books(ISBN_number='1234567891012', 
                      author='Rohan', 
                      book_title='Very Good Book2',
                      price=900, 
                      available_number=20, 
                      publisher=publisher1, 
                      genre=genre2
                      )
        
        book3 = Books(ISBN_number='1234567891013', 
                      author='Rohan', 
                      book_title='Very Good Book3',
                      price=1000, 
                      available_number=10, 
                      publisher=publisher1, 
                      genre=genre3
                      )
        
        magazine1 = Magazine(ISSN_number='12345678', 
                             editor='Rohan', 
                             magazine_title='Very Good Magazine',
                             price=800, available_number=10, 
                             publisher=publisher2, 
                             genre=genre1
                             )
        
        user1 = User(username='username1', 
                     email='email1', 
                     address='address',
                     phone_number=5678910111213, 
                     book_id=[book1, book3]
                     )
        
        user2 = User(username='username2', 
                     email='email2', 
                     address='address',
                     phone_number=5678910111214, 
                     book_id=[book2, book3], 
                     magazine_id=[magazine1]
                     )
        
        session.add_all([genre1, genre2, genre3, book1, book2,
                        book3, magazine1, user1, user2])
        
        record_to_add = Record(user=user1, 
                               book=book1, 
                               genre=book1.genre, 
                               issued_date=datetime.utcnow().date()
                               )
        
        record_to_add2 = Record(user=user1, 
                                book=book2, 
                                genre=book2.genre, 
                                issued_date=datetime.utcnow().date()
                                )
        
        record_to_add3 = Record(user=user1, 
                                magazine=magazine1,
                                genre=magazine1.genre, 
                                issued_date=datetime.utcnow().date()
                                )
        
        record_to_add4 = Record(
            user=user2, 
            book=book2, 
            genre=book2.genre, 
            issued_date=datetime.utcnow().date(), 
            expected_return_date=(datetime.utcnow().date() + timedelta(days=30)))
        
        record_to_add5 = Record(
            user=user2, 
            book=book3, 
            genre=book3.genre, 
            issued_date=datetime.utcnow().date(), 
            expected_return_date=(datetime.utcnow().date() + timedelta(days=30))
                                )
        
        librarian1 = Librarian(
            name='Kausha Gautam',
            email='admin1@lms.com',
            password='supersecuredangerpassword',
            address='Kathmandu',
            phone_number=9810234567,
        )
        
        librarian2 = Librarian(
            name='Sakar Poudel',
            email='admin@lms.com',
            password='admin',
            address='Kathmandu',
            phone_number=9810234567,
        )

        session.add_all([
            record_to_add,
            record_to_add2,
            record_to_add3,
            record_to_add4,
            record_to_add5,
            librarian1,
            librarian2
        ])
        session.commit()

def try_session_commit(session):
    try:
        session.commit()
    except IntegrityError as e:
        print(e._message())
        session.rollback()
        print("Rolling back all the transaction and redirecting to\
            main menu, please wait")
        time.sleep(5)