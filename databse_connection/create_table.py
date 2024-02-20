from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey
from datetime import datetime, timedelta
from connect_db import engine

# Base = declarative_base()
class Base(DeclarativeBase):
    pass


session = Session(bind=engine)

class MemberBooks(Base):
    __tablename__ = 'member_book'
    id = Column(Integer, primary_key = True)
    user_id = Column('user_id',Integer, ForeignKey('users.id'))
    book_id = Column('book_id',String, ForeignKey('books.ISBN_number'))
    
    def __str__(self) -> str:
        return f'{self.user_id} and {self.id}'
    
class MemberMagazine(Base):
    __tablename__ = 'member_magazine'
    id = Column(Integer, primary_key = True)
    user_id = Column('user_id',Integer, ForeignKey('users.id'))
    magazine_id = Column('magazine_id',String, ForeignKey('magazines.ISSN_number'))
    
    def __str__(self) -> str:
        return f'{self.user_id} and {self.id}'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(),primary_key=True)
    username= Column(String(50), nullable= False, unique= True)
    email = Column(String(50), nullable=False)
    date_created = Column(DateTime(),default=datetime.utcnow().date())
    expiry_date = Column(DateTime(), default= datetime.utcnow().date() + timedelta(days=60))
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    book_id = relationship('Books', secondary='member_book', back_populates='user_id')
    magazine_id = relationship('Magazine', secondary='member_magazine', back_populates='user_id')
    
    def __str__(self):
        return f'{self.__tablename__}'
    
class Books(Base):
    __tablename__='books'
    ISBN_number = Column(String(15),nullable = False, unique = True, primary_key=True, autoincrement=False)
    book_title = Column(String(100), nullable=False)
    author = Column(String(20),nullable= False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship('User', secondary='member_book', back_populates='book_id')
    # genre_id = Column(Integer(), ForeignKey('genre.id'))
    genre = relationship('Genre', sync_backref='genre')
    
    def __str__(self):
        return f'{self.__tablename__}'
    
class Magazine(Base):
    __tablename__='magazines'
    ISSN_number = Column(String(15),nullable = False, unique = True, primary_key=True, autoincrement=False)
    magazine_title = Column(String(100), nullable=False)
    editor = Column(String(20),nullable= False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship('User', secondary='member_magazine', back_populates='magazine_id')
    
    def __str__(self):
        return f'{self.__tablename__}'
      
class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer(),primary_key = True)
    genre_name = Column(String(50), nullable = False)
    book_id = Column(String(15),ForeignKey('books.ISBN_number'))
     
    def __str__(self):
        return f'{self.__tablename__}'
    
class Librarian(Base):
    __tablename__ = 'librarians'
    id = Column(Integer(),primary_key=True)
    name= Column(String(50), nullable= False, unique= True)
    email = Column(String(50), unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    
    def __str__(self):
        return f'{self.__tablename__}'
    
# class Record(Base):
#     __tablename__ = 'records'
#     record_id = Column(Integer(), primary_key = True)
#     member_id = Column()
#     book_id = Column()
    
    

# def init_database(engine):
#     Base.metadata.create_all(engine)

Base.metadata.create_all(engine)
book1 = Books(ISBN_number = '1234567891011', author='Rohan',book_title='Very Good Book', price=800)
book2 = Books(ISBN_number = '1234567891012', author='Rohan',book_title='Very Good Book2', price=900)
book3 = Books(ISBN_number = '1234567891013', author='Rohan',book_title='Very Good Book3', price=1000)
magazine1 = Magazine(ISSN_number = '1234567891011', editor='Rohan',magazine_title='Very Good Magazine', price=800)
user1 = User(username='username1',email='email1',address='address',phone_number=5678910111213, book_id=[book1,book3])
user2 = User(username='username2',email='email2',address='address',phone_number=5678910111214, book_id=[book2,book3], magazine_id=[magazine1])

session.add_all([book1, book2, book3,magazine1,user1,user2])
# session.add(user1)

session.commit()



