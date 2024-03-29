import time
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey, Boolean
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from cli_components import try_convert_to_int, columns
import os
from sqlalchemy import text, create_engine, URL, inspect
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from cli_components import error_assci




def try_session_commit(session):
    try:
        session.commit()
    except IntegrityError as e:
        print(e._message())
        session.rollback()
        print("Rolling back all the transaction and redirecting to\
            main menu, please wait")
        time.sleep(5)

class CustomDatabaseException(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)


class Base(DeclarativeBase):
    pass


class MemberBook(Base):
    __tablename__ = 'member_book'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    book_id = Column('book_id', String, ForeignKey('books.isbn_number'))

    
class MemberMagazine(Base):
    __tablename__ = 'member_magazine'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    magazine_id = Column('magazine_id', String,
                         ForeignKey('magazines.issn_number'))


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
    fine = Column(Integer, default=0)
    book_id = relationship(
        'Book', secondary='member_book', back_populates='user_id')
    magazine_id = relationship(
        'Magazine', secondary='member_magazine', back_populates='user_id')
    record = relationship('Record', backref='user')
    
    def __init__(self, username, email, address, phone_number, book_id=None, magazine_id =None) -> None:
        self.username = username
        self.email = email
        self.address = address
        self.phone_number = phone_number
        if book_id:
            self.book_id = book_id
        if magazine_id:
            self.magazine_id = magazine_id
        
    
    def add(self):
        session.add(self)
        try_session_commit(session)
        
 
    def get_user_object(self):
        return session.query(User).where(
                User.username == self.username).one()        

        
    def add_book(self, isbn_number, days=15):
        book_to_add = session.query(Book).where(
            Book.isbn_number == isbn_number).one_or_none()
        if not book_to_add:
            raise CustomDatabaseException(
                f"No Book with the ISBN number {isbn_number}")
        
        user_object = self.get_user_object()
        
        user_object.book_id += [book_to_add]
        book_to_add.available_number -= 1
        user_already_exsist = session.query(Record).where(
            Record.book_id == book_to_add.isbn_number,
            Record.member_id == user_object.id,
            Record.returned == False
        ).count()
        if not user_already_exsist and book_to_add.available_number > 0:
            book_record = Record(
                user=user_object, book=book_to_add,
                genre=book_to_add.genre, issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(book_record)
            try_session_commit(session)
        elif book_to_add.available_number == 0:
            raise CustomDatabaseException(
                "This book is curently out of stock, please check again after some days.")

        else:
            raise CustomDatabaseException(
                "You have already issued this same book already.")
        
    
    def add_magazine(self, issn_number, days=15):
        
        magazine_to_add = session.query(Magazine).where(
            Magazine.issn_number == issn_number).one_or_none()
        if not magazine_to_add:
            raise CustomDatabaseException(
                f"No Magazine with the ISSN number {issn_number}")
            
        user_object = self.get_user_object()
        user_object.magazine_id += [magazine_to_add]
        user_already_exsist = session.query(Record).where(
            Record.magazine_id == magazine_to_add.issn_number,
            Record.member_id == user_object.id,
            Record.returned == False
        ).count()
        
        if not user_already_exsist and magazine_to_add.available_number > 0:
            magazine_to_add.available_number -= 1
            magazine_record = Record(
                user=user_object,
                magazine=magazine_to_add,
                genre=magazine_to_add.genre,
                issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(magazine_record)
            try_session_commit(session)
        elif magazine_to_add.available_number == 0:
            raise CustomDatabaseException(
                "This Magazine is curently out of stock, please check again after some days.")

        else:
            raise CustomDatabaseException(
                "You have already issued this same magazine already.")
     
     
    def calculate_fine(self):
        user_object = self.get_user_object()
        borrowed_records = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.returned == False
        ).all()
        user_object.fine = 0
        expired_books_or_magazine = []
        if borrowed_records:
            for each_record in borrowed_records:

                if each_record.expected_return_date.date() < datetime.utcnow().date():
                    extra_days = (datetime.utcnow().date() -
                                  each_record.expected_return_date.date()).days
                    if each_record.book:
                        expired_books_or_magazine.append(
                            [str(each_record.book.title) + " Book",
                             each_record.expected_return_date.date()]
                        )
                    if each_record.magazine:
                        expired_books_or_magazine.append(
                            [str(each_record.magazine.title) +
                             " Magazine", each_record.expected_return_date.date()]
                        )
                    if extra_days > 3:
                        fine = extra_days * 3
                        user_object.fine += fine
                        try_session_commit(session)
            return expired_books_or_magazine 
     

    def return_book(self, isbn_number):

            book_to_return = session.query(Book).where(
                Book.isbn_number == isbn_number).one_or_none()
            if not book_to_return:
                raise CustomDatabaseException(
                    f"No Book with the ISBN number {isbn_number}")
                
            user_object = self.get_user_object()
            got_record = session.query(Record).where(
                Record.member_id == user_object.id,
                Record.book_id == isbn_number,
                Record.returned == False
            ).one_or_none()

            if got_record:
                # user_object
                books_record = session.query(Record).filter(
                    Record.member_id == user_object.id,
                    Record.book_id == isbn_number,
                    Record.returned == False
                ).one()
                if books_record.expected_return_date.date() < datetime.utcnow().date():

                    extra_days = (datetime.utcnow().date() -
                                  books_record.expected_return_date.date()).days
                    if extra_days > 3:
                        fine = extra_days * 3
                        self.pay_fine(fine_remaning=fine)
                        user_object.fine = 0

                        # try_session_commit(session)
                book_to_return.available_number += 1
                books_record.returned = True
                # books_record.returned_date = datetime.utcnow().date()
                
                session.query(MemberBook).filter(
                    MemberBook.book_id == isbn_number,
                    MemberBook.user_id == user_object.id
                ).delete()

            else:
                raise CustomDatabaseException(
                    f"The user {self.username} haven't issued book {book_to_return.title}")
            try_session_commit(session)


    def return_magazine(self, issn_number):
        
        magazine_to_return = session.query(Magazine).where(
            Magazine.issn_number == issn_number).one_or_none()

        if not magazine_to_return:
            raise CustomDatabaseException(
                f"No Magazine with the ISSN number {issn_number}")
            
        user_object = self.get_user_object()
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.magazine_id == issn_number,
            Record.returned == False
        ).one_or_none()
        if got_record:

            magazine_record = session.query(Record).filter(
                Record.member_id == user_object.id,
                Record.magazine_id == issn_number,
                Record.returned == False
            ).one()
            if magazine_record.expected_return_date.date() < datetime.utcnow().date():

                extra_days = (magazine_record.expected_return_date.date(
                ) - datetime.utcnow().date()).days
                if extra_days > 3:
                    fine = extra_days * 3
                    self.pay_fine(fine)

            magazine_to_return.available_number += 1
            magazine_record.returned = True
            # magazine_record.returned_date = datetime.utcnow().date()

            session.query(MemberMagazine).filter(
                MemberMagazine.magazine_id == issn_number,
                MemberMagazine.user_id == user_object.id
            ).delete()
        else:
            raise CustomDatabaseException(
                f"The user {self.username} haven't issued that magazine")
        try_session_commit(session)


    @classmethod
    def instance_from_username(cls,username):
        User.email
        user_object = session.query(User).where(
            User.username == username).one_or_none()
        if user_object:
            object = cls(
                username=username,
                email=user_object.email,
                address=user_object.address,
                phone_number=user_object.phone_number
            )
            return object.get_user_object()

        else:
            raise CustomDatabaseException("No such UserName")

        
    @staticmethod   
    def show_all_members():
        all_member_list = []
    
        members = session.query(User).all()
        for member in members:
            member_book_list = [book.title for book in member.book_id]
            member_magazine_list = [
                magazine.title for magazine in member.magazine_id]
            new_list = [
                member.username,
                member.expiry_date.date(),
                member_book_list,
                member_magazine_list
            ]
            all_member_list.append(new_list)
        return all_member_list


    @staticmethod
    def pay_fine(fine_remaning):
        while fine_remaning != 0:
            if fine_remaning > 0:
                print(
                    f"You have Rs{fine_remaning} fee remaning".center(columns))
                given_payment = try_convert_to_int("Enter the fine ammount: ")
                fine_remaning = fine_remaning - given_payment
            elif fine_remaning < 0:
                print(
                    f"You have Rs{fine_remaning * -1} fee overpaid".center(columns))
                print("\n Returned the money")
                input("All fine paid, Thanks you".center(columns))
                fine_remaning = 0
            else:
                input("All fine paid, Thanks you".center(columns))
                break
    


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(200))
    phone_number = Column(BigInteger())
    books = relationship('Book', backref='publisher')
    magazine = relationship('Magazine', backref='publisher')
    
    def __init__(self, name, address=None, phone_number=None):
        # unique constraint
        self.name = name
        if phone_number:
            self.phone_number = phone_number
        if address:
            self.address= address
        
        
    def add(self):
        session.add(self)
        try_session_commit(session)
        
    
    def get_publisher_object(self):
        return session.query(Publisher).where(Publisher.id == self.name).one_or_none()

    @staticmethod
    def show_all_publisher():
        publishers_list = []
        publishers = session.query(Publisher).all()
        for publisher in publishers:
            publisher_list = [
                publisher.id,
                publisher.name,
                publisher.address,
                publisher.phone_number
            ]

            publishers_list.append(publisher_list)
        return (publishers_list)

class Book(Base):
    __tablename__ = 'books'
    isbn_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    title = Column(String(100), nullable=False)
    author = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_book', back_populates='book_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='book')

    def __init__(self, isbn_number, author, title,
                 price, available_number, publisher, genre):
        self.isbn_number = isbn_number
        self.author=author
        self.title = title
        self.price = price
        self.available_number = available_number
        self.publisher = publisher
        self.genre = genre
        self.add()
        
        
    def add(self):
        session.add(self)
        try_session_commit(session)
        
        
    @staticmethod
    def show_all_book():
        books_list = []
        books = session.query(Book).all()
        for book in books:
            
            book_list = [
                book.isbn_number,
                book.title,
                book.author,
                book.price,
                book.available_number,
                book.publisher.name,
                book.genre.name
            ]
            books_list.append(book_list)
        return books_list
    
    @staticmethod
    def get_unreturned_user_books(user_id):
        # TODO: retrieve time taken to perform below operation
        # add dummy data in order to make this table huge, then see how your query performs
        books_list = []
        books = session.query(Book).where(
            Book.user_id.contains(user_id)).all()
        if books:
            for book in books:
                not_returned = session.query(
                    Record
                ).where(
                    Record.member_id == user_id.id,
                    Record.book_id == book.isbn_number,
                    Record.returned == False
                ).one_or_none()

                if not_returned:
                    
                    book_list = [
                        book.isbn_number,
                        book.title,
                        book.author,
                        book.price,
                        book.available_number,
                        book.publisher.name,
                        book.genre.name
                    ]
                    books_list.append(book_list)
        else:
            books_list = [[]]
        return books_list
        
        
class Magazine(Base):
    __tablename__ = 'magazines'
    issn_number = Column(String(15), nullable=False,
                         unique=True, primary_key=True, autoincrement=False)
    title = Column(String(100), nullable=False)
    editor = Column(String(20), nullable=False, default='Folklore')
    price = Column(Integer(), nullable=False)
    user_id = relationship(
        'User', secondary='member_magazine', back_populates='magazine_id')
    genre_id = Column(Integer(), ForeignKey('genre.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    available_number = Column(Integer, default=0)
    record = relationship('Record', backref='magazine')
    
    def __init__(self, issn_number, editor, title,
                 price, available_number, publisher, genre):
        self.issn_number = issn_number
        self.editor = editor
        self.title = title
        self.price = price
        self.available_number = available_number
        self.publisher = publisher
        self.genre = genre
        
    def add(self):
        session.add(self)
        try_session_commit(session)
        
    @staticmethod
    def show_all_magazine():
        magazines_list = []
        magazines = session.query(Magazine).all()
        for magazine in magazines:
            magazine_list = [
                magazine.issn_number,
                magazine.title,
                magazine.editor,
                magazine.price,
                magazine.available_number,
                magazine.publisher.name,
                magazine.genre.name
            ]
            magazines_list.append(magazine_list)
        return magazines_list

    @staticmethod
    def show_users_all_magazine(user_id):
        magazines_list = []
        magazines = session.query(Magazine).where(
            Magazine.user_id.contains(user_id)).all()
        if magazines:
            for magazine in magazines:
                magazine_list = [
                    magazine.issn_number,
                    magazine.title,
                    magazine.editor,
                    magazine.price,
                    magazine.available_number,
                    magazine.publisher.name,
                    magazine.genre.name
                ]
                magazines_list.append(magazine_list)
        else:
            magazines_list = [[]]
        return magazines_list


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    books = relationship('Book', backref='genre')
    magazine = relationship('Magazine', backref='genre')
    record = relationship('Record', backref='genre')
    
    def __init__(self, name) -> None:
        self.name = name
        # genre_exsist = session.query(Genre).where(
        #     Genre.name == name).count()
        # if not genre_exsist:
        #     new_genre = Genre(name=name)
        #     session.add(new_genre)
        #     try_session_commit(session)
        # else:
        #     print(
        #         f"The Genre with the name {name} already exsit, cant add it again")
        #     input("Press any key to continue: ")

    def add(self):
        session.add(self)
        try_session_commit(session)
    
    @staticmethod
    def show_all_genre():
        genre_lists = []
        
        genres = session.query(Genre).all()
        for genre in genres:
            genre_list = [genre.id, genre.name]
            genre_lists.append(genre_list)
        return genre_lists

    @staticmethod
    def get_genre_object(name):
        return session.query(Genre).where(Genre.id == name).one_or_none()


class Librarian(Base):
    __tablename__ = 'librarians'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(BigInteger())
    
    def __init__(self, name, email, password, address, phone_number):
        librarian1 = Librarian(
            name=name,
            email=email,
            password=password,
            address=address,
            phone_number=phone_number
        )
        session.add(librarian1)
        try_session_commit(session)

    @staticmethod
    def librarian_login(email, password):
        librarian_object = session.query(Librarian).where(
            Librarian.email == email,
            Librarian.password == password
        ).one_or_none()
        if librarian_object:
            return True, librarian_object.name
        return False, None



class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer(), primary_key=True)
    member_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(String, ForeignKey('books.isbn_number'))
    magazine_id = Column(String, ForeignKey('magazines.issn_number'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    issued_date = Column(DateTime(), default=datetime.utcnow().date())
    returned_date = Column(DateTime(), default=datetime.utcnow().date())
    expected_return_date = Column(DateTime(), default=(
        datetime.utcnow().date() + timedelta(days=15)))
    returned = Column(Boolean, default=False)


def create_database(engine, dummy_data):
    Base.metadata.create_all(engine)
    if dummy_data:

        educational = Genre(name='Educational')
        action = Genre(name='Action')
        folktale = Genre(name='Folktale')
        kantipur = Publisher(
            name="Kantipur Publishers",
            address="Kathmandu",
            phone_number=9810204567
        )

        ekata = Publisher(
            name="Ekata Publishers",
            address="Pokhara",
            phone_number=9810204527
        )

        cant_hurt_me = Book(isbn_number='1234567891011',
                      author='Rohan',
                      title='Cant Hurt Me',
                      price=800,
                      available_number=50,
                      publisher=kantipur,
                      genre=educational
                      )

        kafka_on_sore = Book(isbn_number='1234567891012',
                      author='Rohan',
                      title='Kafka On Sore',
                      price=900,
                      available_number=20,
                      publisher=kantipur,
                      genre=action
                      )

        kite_runner = Book(isbn_number='1234567891013',
                      author='Rohan',
                      title='The Kite Runner',
                      price=1000,
                      available_number=10,
                      publisher=kantipur,
                      genre=folktale
                      )

        the_new_york_times = Magazine(issn_number='12345678',
                             editor='Rohan',
                             title='The New York Times',
                             price=800, 
                             available_number=10,
                             publisher=ekata,
                             genre=educational
                             )

        kaushal = User(username='kaushal',
                    session = session,
                    email='email1',
                    address='address',
                    phone_number=5678910111213,
                    book_id=[cant_hurt_me, kite_runner]
                    )

        ganesh = User(username='ganesh',
                    session=session,
                    email='email2',
                    address='address',
                    phone_number=5678910111214,
                    book_id=[kafka_on_sore, kite_runner],
                    magazine_id=[the_new_york_times]
                    )

        session.add_all([educational, action, folktale, cant_hurt_me, kafka_on_sore,
                        kite_runner, the_new_york_times, kaushal, ganesh])

        kaushal_cant_hurt_me = Record(user=kaushal,
                               book=cant_hurt_me,
                               genre=cant_hurt_me.genre,
                               issued_date=datetime.utcnow().date()
                               )

        kaushal_kafka = Record(user=kaushal,
                                book=kafka_on_sore,
                                genre=kafka_on_sore.genre,
                                issued_date=datetime.utcnow().date()
                                )

        kaushal_newyork_times = Record(user=kaushal,
                                magazine=the_new_york_times,
                                genre=the_new_york_times.genre,
                                issued_date=datetime.utcnow().date()
                                )

        ganesh_kafka = Record(
            user=ganesh,
            book=kafka_on_sore,
            genre=kafka_on_sore.genre,
            issued_date=datetime.utcnow().date(),
            expected_return_date=(datetime.utcnow().date() + timedelta(days=30)))

        ganesh_kite_runner = Record(
            user=ganesh,
            book=kite_runner,
            genre=kite_runner.genre,
            issued_date=datetime.utcnow().date(),
            expected_return_date=(
                datetime.utcnow().date() + timedelta(days=30))
        )

        kaushal_librarian = Librarian(
            name='Kausha Gautam',
            email='admin1@lms.com',
            password='supersecuredangerpassword',
            address='Kathmandu',
            phone_number=9810234567,
        )

        session.add_all([
            kaushal_cant_hurt_me,
            kaushal_kafka,
            kaushal_newyork_times,
            ganesh_kafka,
            ganesh_kite_runner,
            kaushal_librarian,

        ])
        sakar_librarian = Librarian(
            name='Sakar Poudel',
            email='admin@lms.com',
            password='admin',
            address='Kathmandu',
            phone_number=9810234567,
        )
        session.add(sakar_librarian)
        session.commit()

load_dotenv()

host = os.getenv('host')
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')


url = URL.create(
    database=database,
    username=user,
    password=password,
    host=host,
    drivername="postgresql"
)
engine = create_engine(url)
session = Session(bind=engine)
tables = inspect(engine).get_table_names()

if len(tables) < 9:
    error_assci()
    print("Incomplete Database found, Deleting the database to create a new one from scratch")
    print("Do you want to continue??(Y/N)")
    user_in = input("\n\t:").strip().lower()
    if user_in == 'n':
        exit()
    dummy_data = False
    dummy = input("Do you want a dummy data on databse?(y/n)").strip().lower()
    if dummy == 'y':
        dummy_data = True
    if tables:
        table_string = ", ".join(tables)
        session.execute(text(f"DROP TABLE {table_string};"))
    create_database(engine,  dummy_data, session,)
    print("Database Created")

