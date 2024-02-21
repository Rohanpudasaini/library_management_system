from datetime import datetime, timedelta
from databse_connection.connect_db import Librarian, Magazine, MemberBooks, User, Books, \
    Publisher, Record, MemberMagazine, session, try_session_commit, Genre
from sqlalchemy.exc import IntegrityError



class Members():
    def __init__(self, username, email, address, phone_number) -> None:
        user_to_add = User(username=username, email=email,
                           address=address, phone_number=phone_number)
        session.add(user_to_add)
        try_session_commit(session)

    @staticmethod
    def user_add_book(username, ISBN_number, days=15):
        book_to_add = session.query(Books).where(
            Books.ISBN_number == ISBN_number).one()
        user_object = session.query(User).where(
            User.username == username).one()
        user_object.book_id = [book_to_add]
        book_to_add.available_number -= 1
        user_already_exsist = session.query(Record).where(
            Record.book_id == book_to_add.ISBN_number,
            Record.member_id == user_object.id
        ).count()
        if not user_already_exsist and book_to_add.available_number > 0:
            record_to_add = Record(
                user=user_object, book=book_to_add,
                genre=book_to_add.genre, issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(record_to_add)
            try_session_commit(session)
        elif book_to_add.available_number == 0:
            print(
                "This book is curently out of stock, please check again after some days.")

        else:
            print("You have already issued this same book already.")

    @staticmethod
    def user_add_magazine(username, ISSN_number, days=15):
        magazine_to_add = session.query(Magazine).where(
            Magazine.ISSN_number == ISSN_number).one()
        user_object = session.query(User).where(
            User.username == username).one()
        user_object.magazine_id = [magazine_to_add]
        magazine_to_add.available_number -= 1
        record_to_add = Record(
            user=user_object, magazine=magazine_to_add,
            genre=magazine_to_add.genre, issued_date=datetime.utcnow().date(),
            expected_return_date=(
                datetime.utcnow().date() + timedelta(days=days))
        )
        session.add(record_to_add)
        try_session_commit(session)

    @staticmethod
    def user_return_book(username, ISBN_number):
        book_to_return = session.query(Books).where(
            Books.ISBN_number == ISBN_number).one()
        user_object = session.query(User).where(
            User.username == username).one()
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.book_id == ISBN_number
        ).all()
        if got_record:
            book_to_return.available_number += 1
            session.query(Record).filter(Record.member_id ==
                                         user_object.id, Record.book_id == ISBN_number).delete()
        else:
            print(
                f"The user {username} haven't issued book {book_to_return.book_title}")
        try_session_commit(session)

    @staticmethod
    def user_return_magazine(username, ISSN_number):
        magazine_to_return = session.query(Magazine).where(
            Magazine.ISBN_number == ISSN_number).one()
        user_object = session.query(User).where(
            User.username == username).one()
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.magazine_id == ISSN_number
        ).all()
        if got_record:
            magazine_to_return.available_number += 1
            session.query(Record).filter(
                Record.member_id == user_object.id, Record.magazine_id == ISSN_number).delete()
        else:
            print(
                f"The user {username} haven't issued magazine {magazine_to_return.magazine_title}")
        try_session_commit(session)
        
    @staticmethod
    def is_member(username):
        user_object_count = session.query(User).where(
            User.username == username).count()
        user_object = None
        if user_object_count:
            user_object = session.query(User).where(
                User.username == username
            ).one()
        return user_object_count, user_object
    
    @staticmethod
    def show_all_members():
        all_member_list = []
        header = ['Username', 'Membership Expiry date', 'Books Issued', 'Magazine Issued']
        members = session.query(User).all()
        for member in members:
            member_book_list = [book.book_title for book in member.book_id]
            member_magazine_list = [magazine.magazine_title for magazine in member.magazine_id]
            new_list = [member.username, member.expiry_date.date(), member_book_list, member_magazine_list]
            all_member_list.append(new_list)
        return (all_member_list, header)
            
        
        


class Book:

    def __init__(self, ISBN_number, author, book_title, price, available_number) -> None:
        book1 = Books(ISBN_number=ISBN_number, author=author, book_title=book_title,
                      price=price, available_number=available_number)
        session.add(book1)
        try_session_commit(session)
    

class Library_Admin:
    
    def __init__(self, name, email, password, address, phone_number) -> None:
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
            
class Publications:
    def __init__(self,name,address,phone_number):
        publisher_to_add = Publisher(
            name = name,
            address = address,
            phone_number = phone_number
        )
        session.add(publisher_to_add)
        try_session_commit(session)
        
    @staticmethod
    def show_all_publisher():
        publishers_list = []
        header_list = ["ID","Name", "Address", "Phone Number"]
        publishers = session.query(Publisher).all()
        for publisher in publishers:
            publisher_list = [publisher.id,publisher.name, publisher.address, publisher.phone_number]
            publishers_list.append(publisher_list)
        return (publishers_list, header_list)
    
class GenreClass():
    def __init__(self, name) -> None:
        new_genre = Genre(genre_name=name)
        session.add(new_genre)
        try_session_commit(session)

    @staticmethod
    def show_all_genre():
        genre_lists = []
        header_list = ["ID", "Name"]
        genres = session.query(Genre).all()
        for genre in genres:
            genre_list = [genre.id, genre.genre_name]
            genre_lists.append(genre_list)
        return (genre_lists,header_list)