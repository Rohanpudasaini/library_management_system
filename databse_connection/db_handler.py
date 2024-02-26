from datetime import datetime, timedelta
from cli_components import try_convert_to_int
from databse_connection.connect_db import Librarian, Magazine,  User, Books, \
    Publisher, Record, session, try_session_commit, Genre, MemberBooks, MemberMagazine, \
    NoResultFound
import shutil
columns = shutil.get_terminal_size().columns


class Members():
    def __init__(self, username, email, address, phone_number) -> None:
        member_to_add = User(username=username, email=email,
                             address=address, phone_number=phone_number)
        session.add(member_to_add)
        try_session_commit(session)

    @staticmethod
    def member_add_book(username, ISBN_number, days=15):
        try:
            book_to_add = session.query(Books).where(
                Books.ISBN_number == ISBN_number).one()
        except NoResultFound:
            print(f"No Book with the ISBN number {ISBN_number}")
            input("Press any key to continue")
            return
        user_object = session.query(User).where(
            User.username == username).one()
        user_object.book_id += [book_to_add]
        book_to_add.available_number -= 1
        user_already_exsist = session.query(Record).where(
            Record.book_id == book_to_add.ISBN_number,
            Record.member_id == user_object.id,
            Record.returned == False
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
            input("Press any key to continue")

    @staticmethod
    def member_add_magazine(username, ISSN_number, days=15):
        try:
            magazine_to_add = session.query(Magazine).where(
                Magazine.ISSN_number == ISSN_number).one()
        except NoResultFound:
            print(f"No Magazine with the ISSN number {ISSN_number}")
            input("Press any key to continue")
            return
        user_object = session.query(User).where(
            User.username == username).one()
        user_object.magazine_id += [magazine_to_add]
        user_already_exsist = session.query(Record).where(
            Record.magazine_id == magazine_to_add.ISSN_number,
            Record.member_id == user_object.id,
            Record.returned == False
        ).count()
        if not user_already_exsist and magazine_to_add.available_number > 0:
            magazine_to_add.available_number -= 1
            record_to_add = Record(
                user=user_object,
                magazine=magazine_to_add,
                genre=magazine_to_add.genre,
                issued_date=datetime.utcnow().date(),
                expected_return_date=(
                    datetime.utcnow().date() + timedelta(days=days))
            )
            session.add(record_to_add)
            try_session_commit(session)
        elif magazine_to_add.available_number == 0:
            print(
                "This Magazine is curently out of stock, please check again after some days.")

        else:
            print("You have already issued this same magazine already.")
            input("Press any key to continue")

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
        header = ['Username', 'Membership Expiry date',
                  'Books Issued', 'Magazine Issued']
        members = session.query(User).all()
        for member in members:
            member_book_list = [book.book_title for book in member.book_id]
            member_magazine_list = [
                magazine.magazine_title for magazine in member.magazine_id]
            new_list = [
                member.username,
                member.expiry_date.date(),
                member_book_list,
                member_magazine_list
            ]
            all_member_list.append(new_list)
        return (all_member_list, header)

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

    @staticmethod
    def calculate_fine(user_object):
        borrowed_records = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.returned == False
        ).all()
        user_object.fine = 0

        if borrowed_records:
            for each_record in borrowed_records:

                if each_record.expected_return_date.date() < datetime.utcnow().date():
                    extra_days = (datetime.utcnow().date() -
                                  each_record.expected_return_date.date()).days

                    if extra_days > 3:
                        fine = extra_days * 3
                        user_object.fine += fine
                        try_session_commit(session)

    @classmethod
    def member_return_book(cls, username, ISBN_number):
        try:
            book_to_return = session.query(Books).where(
                Books.ISBN_number == ISBN_number).one()
        except NoResultFound:
            print(f"No Book with the ISBN number {ISBN_number}")
            input("Press any key to continue")
            return
        user_object = session.query(User).where(
            User.username == username).one()
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.book_id == ISBN_number,
            Record.returned == False
        ).one_or_none()

        if got_record:
            # user_object
            books_record = session.query(Record).filter(
                Record.member_id == user_object.id,
                Record.book_id == ISBN_number,
                Record.returned == False
            ).one()
            if books_record.expected_return_date.date() < datetime.utcnow().date():

                extra_days = (datetime.utcnow().date()- books_record.expected_return_date.date()).days 
                if extra_days > 3:
                    fine = extra_days * 3
                    cls.pay_fine(fine_remaning=fine)
                    user_object.fine = 0

                    # try_session_commit(session)
            book_to_return.available_number += 1
            books_record.returned = True
            books_record.returned_date = datetime.utcnow().date()

            session.query(MemberBooks).filter(
                MemberBooks.book_id == ISBN_number,
                MemberBooks.user_id == user_object.id
            ).delete()

        else:
            print(
                f"The user {username} haven't issued book {book_to_return.book_title}")
        try_session_commit(session)

    @classmethod
    def member_return_magazine(cls, username, ISSN_number):
        try:
            magazine_to_return = session.query(Magazine).where(
                Magazine.ISSN_number == ISSN_number).one_or_none()

        except NoResultFound:
            print(f"No Magazine with the ISSN number {ISSN_number}")
            input("Press any key to continue")
            return
        user_object = session.query(User).where(
            User.username == username).one()
        got_record = session.query(Record).where(
            Record.member_id == user_object.id,
            Record.magazine_id == ISSN_number,
            Record.returned == False
        ).one_or_none()
        if got_record:

            magazine_record = session.query(Record).filter(
                Record.member_id == user_object.id,
                Record.magazine_id == ISSN_number,
                Record.returned == False
            ).one()
            if magazine_record.expected_return_date.date() < datetime.utcnow().date():

                extra_days = (magazine_record.expected_return_date.date(
                ) - datetime.utcnow().date()).days
                if extra_days > 3:
                    fine = extra_days * 3
                    cls.pay_fine(fine)

            magazine_to_return.available_number += 1
            magazine_record.returned = True
            magazine_record.returned_date = datetime.utcnow().date()

            session.query(MemberMagazine).filter(
                MemberMagazine.magazine_id == ISSN_number,
                MemberMagazine.user_id == user_object.id
            ).delete()
        else:
            print(
                f"The user {username} haven't issued that magazine")
            input("Press any key to continue..")
        try_session_commit(session)


class Book:

    def __init__(self, ISBN_number, author, book_title,
                 price, available_number, publication, genre):
        book1 = Books(
            ISBN_number=ISBN_number,
            author=author,
            book_title=book_title,
            price=price,
            available_number=available_number,
            publisher=publication,
            genre=genre
        )

        session.add(book1)
        try_session_commit(session)

    @staticmethod
    def show_all_book():
        books_list = []
        header = ["ISBN Number", "Title", "Author", "Price",
                  "Available number", "Publisher", "Genre"
                  ]
        books = session.query(Books).all()
        for book in books:
            book_list = [
                book.ISBN_number,
                book.book_title,
                book.author,
                book.price,
                book.available_number,
                book.publisher.name,
                book.genre.genre_name
            ]
            books_list.append(book_list)
        return (books_list, header)

    @staticmethod
    def show_users_all_book(id_given):
        books_list = []
        header = ["ISBN Number", "Title", "Author", "Price",
                  "Available number", "Publisher", "Genre"
                  ]
        books = session.query(Books).where(
            Books.user_id.contains(id_given)).all()
        if books:
            for book in books:
                not_returned = session.query(
                    Record
                    ).where(
                        Record.member_id==1, 
                        Record.book_id=="1234567891013", 
                        Record.returned==False
                        ).one_or_none()
                    
                if not_returned:
                    book_list = [
                        book.ISBN_number,
                        book.book_title,
                        book.author,
                        book.price,
                        book.available_number,
                        book.publisher.name,
                        book.genre.genre_name
                    ]
                    books_list.append(book_list)
        else:
            books_list = [[]]
        return (books_list, header)


class MagazineClass:

    def __init__(self, ISSN_number, editor, magazine_title,
                 price, available_number, publication, genre):

        book1 = Magazine(
            ISSN_number=ISSN_number,
            editor=editor,
            magazine_title=magazine_title,
            price=price,
            available_number=available_number,
            publisher=publication,
            genre=genre
        )

        session.add(book1)
        try_session_commit(session)

    @staticmethod
    def show_all_magazine():
        magazines_list = []
        header = ["ISSN Number", "Title", "Editor", "Price",
                  "Available number", "Publisher", "Genre"]
        magazines = session.query(Magazine).all()
        for magazine in magazines:
            magazine_list = [
                magazine.ISSN_number,
                magazine.magazine_title,
                magazine.editor,
                magazine.price,
                magazine.available_number,
                magazine.publisher.name,
                magazine.genre.genre_name
            ]
            magazines_list.append(magazine_list)
        return (magazines_list, header)

    @staticmethod
    def show_users_all_magazine(user_id):
        magazines_list = []
        header = ["ISSN Number", "Title", "Editor", "Price",
                  "Available number", "Publisher", "Genre"]
        magazines = session.query(Magazine).where(
            Magazine.user_id.contains(user_id)).all()
        if magazines:
            for magazine in magazines:
                magazine_list = [
                    magazine.ISSN_number,
                    magazine.magazine_title,
                    magazine.editor,
                    magazine.price,
                    magazine.available_number,
                    magazine.publisher.name,
                    magazine.genre.genre_name
                ]
                magazines_list.append(magazine_list)
        else:
            magazines_list = [[]]
        return (magazines_list, header)


class Library_Admin:

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


class Publications:
    def __init__(self, name, address, phone_number):
        publication_exsit = session.query(Publisher).where(
            Publisher.name == name).count()
        if not publication_exsit:
            publisher_to_add = Publisher(
                name=name,
                address=address,
                phone_number=phone_number
            )
            session.add(publisher_to_add)
            try_session_commit(session)
        else:
            print(
                f"The Publication with the name {name} already exsit, cant add it again")
            input("Press any key to continue: ")

    @staticmethod
    def show_all_publisher():
        publishers_list = []
        header_list = ["ID", "Name", "Address", "Phone Number"]
        publishers = session.query(Publisher).all()
        for publisher in publishers:
            publisher_list = [
                publisher.id,
                publisher.name,
                publisher.address,
                publisher.phone_number
            ]

            publishers_list.append(publisher_list)
        return (publishers_list, header_list)

    @staticmethod
    def get_publisher_object(publisher_name):
        return session.query(Publisher).where(Publisher.id == publisher_name).one_or_none()


class GenreClass():
    def __init__(self, name) -> None:
        genre_exsist = session.query(Genre).where(
            Genre.genre_name == name).count()
        if not genre_exsist:
            new_genre = Genre(genre_name=name)
            session.add(new_genre)
            try_session_commit(session)
        else:
            print(
                f"The Genre with the name {name} already exsit, cant add it again")
            input("Press any key to continue: ")

    @staticmethod
    def show_all_genre():
        genre_lists = []
        header_list = ["ID", "Name"]
        genres = session.query(Genre).all()
        for genre in genres:
            genre_list = [genre.id, genre.genre_name]
            genre_lists.append(genre_list)
        return (genre_lists, header_list)

    @staticmethod
    def get_genre_object(genre_name):
        return session.query(Genre).where(Genre.id == genre_name).one_or_none()
