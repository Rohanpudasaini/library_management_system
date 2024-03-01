from datetime import datetime, timedelta
from cli_components import try_convert_to_int
from databse_connection.connect_db import Librarian, Magazine,  User, Books, \
    Publisher, Record, session, try_session_commit, Genre, MemberBooks, MemberMagazine, \
    NoResultFound
import shutil
columns = shutil.get_terminal_size().columns







    

    


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


class LibraryAdmin:

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
