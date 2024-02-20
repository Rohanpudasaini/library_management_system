from datetime import datetime, timedelta
from connect_db import Librarian, Magazine, MemberBooks, User, Books,\
    Publisher, Record, MemberMagazine, session, try_session_commit
from sqlalchemy.exc import IntegrityError

class Members():
    def __init__(self, username, email, address, phone_number) -> None:
        user_to_add = User(username=username, email= email, address= address, phone_number= phone_number)
        session.add(user_to_add)
        try_session_commit(session)
        
        
    # @staticmethod
    # def get_student_from_username(username):
    #     user_object = session.query(User).where(User.username == username).one()
    #     return user_object
        
    @staticmethod
    def user_add_book(username,ISBN_number,days=15):
        book_to_add = session.query(Books).where(Books.ISBN_number == ISBN_number).one()
        user_object = session.query(User).where(User.username == username).one()
        user_object.book_id = [book_to_add]
        record_to_add = Record(
            user = user_object, book = book_to_add,
            genre = book_to_add.genre,issued_date = datetime.utcnow().date(),
            expected_return_date=(datetime.utcnow().date() + timedelta(days=days))
        )
        session.add(record_to_add)
        try_session_commit(session)
        
    @staticmethod
    def user_add_magazine(username,ISSN_number,days=15):
        magazine_to_add = session.query(Magazine).where(Magazine.ISSN_number == ISSN_number).one()
        user_object = session.query(User).where(User.username == username).one()
        user_object.magazine_id = [magazine_to_add]
        record_to_add = Record(
            user = user_object, magazine = magazine_to_add,
            genre = magazine_to_add.genre,issued_date = datetime.utcnow().date(),
            expected_return_date=(datetime.utcnow().date() + timedelta(days=days))
        )
        session.add(record_to_add)
        try_session_commit(session)
        
    

# add_user('Testing','test@test.com','kathmandu - 4', 9818234789)

class Book():

    def __init__(self, ISBN_number, author, book_title,price, available_number) -> None:
        book1 = Books(ISBN_number=ISBN_number, author=author, book_title=book_title,
                      price=price, available_number=available_number)
        session.add(book1)
        try:
            session.commit()
        except IntegrityError as e:
            print(e._message())

        
        
