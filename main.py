# from getpass import getpass
from pwinput import pwinput
from os import system
from databse_connection.models import Magazine, User, Book, Librarian, \
    Publisher, Genre
from cli_components import assci_art, issue_book_menu, issue_magazine_menu, librarian_view_choice, \
    main_menu_choice, member_view_choice, book_add_choice, \
    genre_view_choice, magazine_add_choice, add_member_menu, print_center, print_table, \
    publication_view_choice, return_book_menu, return_magazine_menu, columns, show_fine_menu
from time import sleep
logged_in = False
# login_sucess = True

user_header  = ['Username', 'Membership Expiry date',
                  'Books Issued', 'Magazine Issued']

publisher_header = ["ID", "Name", "Address", "Phone Number"]

book_header = ["ISBN Number", "Title", "Author", "Price",
                  "Available number", "Publisher", "Genre"
                  ]

magazine_header = ["ISSN Number", "Title", "Editor", "Price",
                  "Available number", "Publisher", "Genre"]

genre_header = ["ID", "Name"]

assci_art()
user_input = main_menu_choice()
if user_input == '1':
    login_attempt = 5
    while True:

        if not logged_in:
            email = input("Enter your Email: ").strip()
            password = pwinput("Enter your Passkey: ", mask="*")
            login_sucess, librarian_name = Librarian.librarian_login(
                email=email, password=password)

        if login_sucess:
            logged_in = True
            while True:
                user_input = librarian_view_choice(librarian_name)
                if user_input == '0':
                    data = User.show_all_members()
                    print(print_table(data, user_header))
                    input("\n\n Press any key to go back to menu").strip()
                    continue
                if user_input == '1':
                    while True:
                        system("clear")
                        print('\n\n')
                        add_member = input(f"1. Add New Member".center(columns) +
                                           "2. Select Old Member".center(columns) +
                                           "3. Back".center(columns) +
                                           "\n\nEnter your choice: ").strip()

                        if add_member == '1':
                            username, email, address, phone_number = add_member_menu()
                            User(username, email, address, phone_number).add()
                            

                        elif add_member == '2':
                            select_member = input(
                                "Enter the username of the member: ").strip()
                            user_object = User.instance_from_username(
                                select_member)
                            if not user_object:

                                print("No member with that username please check once again\
                                    \nRedirecting to home page")
                                sleep(1.5)
                                continue

                            else:
                                books_or_magazine = user_object.calculate_fine()
                                if user_object.fine > 0:
                                    show_fine_menu(user_object.username, user_object.fine, books_or_magazine)
                                    
                                while True:
                                    user_member_choice = member_view_choice(
                                        user_object.username)
                                    if user_member_choice == '1':
                                        system("clear")
                                        data = Book.show_all_book()
                                        print('\n')
                                        print_center("All Available Book")
                                        print('\n')
                                        print(print_table(data, book_header))
                                        result = issue_book_menu()
                                        if result == None:
                                            continue
                                        ISBN_number_to_issue, days_to_issue = result
                                        user_object.add_book(
                                            ISBN_number_to_issue,
                                            days_to_issue)

                                    elif user_member_choice == '2':
                                        system('clear')
                                        data = Magazine.show_all_magazine()
                                        print('\n')
                                        print_center("All Available Magazine")
                                        print('\n')
                                        print(print_table(data, magazine_header))
                                        result = issue_magazine_menu()
                                        if result == None:
                                            continue
                                        ISSN_number_to_issue, days_to_issue = result
                                        user_object.add_magazine(
                                            ISSN_number_to_issue,
                                            days_to_issue
                                        )

                                    elif user_member_choice == '3':
                                        system('clear')
                                        data = User.show_all_members()
                                        print(print_table(data, user_header))
                                        data = Book.show_all_book()
                                        print(print_table(data, book_header))
                                        ISBN_number_to_return = return_book_menu()
                                        if ISBN_number_to_return == None:
                                            continue
                                        user_object.return_book(
                                            ISBN_number_to_return
                                        )

                                    elif user_member_choice == '4':
                                        system('clear')
                                        data = User.show_all_members()
                                        print(print_table(data, user_header))
                                        data = Magazine.show_all_magazine()
                                        print(print_table(data, magazine_header))
                                        ISSN_number_to_return = return_magazine_menu()
                                        if ISSN_number_to_return == None:
                                            continue
                                        user_object.return_magazine(
                                            ISSN_number_to_return
                                        )

                                    elif user_member_choice == '5':
                                        system('clear')
                                        print("\n\nAll Book")
                                        data = Book.get_unreturned_user_books(
                                            user_object)
                                        print(print_table(data, book_header))
                                        print("\n\nAll Magazine")
                                        data = Magazine.show_users_all_magazine(
                                            user_object)
                                        print(print_table(data, magazine_header))

                                        input("Enter Any key to continue")

                                    else:
                                        break
                        else:
                            break

                elif user_input == '2':
                    system("clear")
                    data = Book.show_all_book()
                    print(print_table(data, book_header))
                    add_book = input("1: Add Book \n2: Back\n\n").strip()

                    if add_book == '1':
                        system("clear")
                        data = Publisher.show_all_publisher()
                        print(print_table(data, publisher_header))
                        print("\n")
                        data = Genre.show_all_genre()
                        print(print_table(data, genre_header))
                        result = book_add_choice()
                        if result == None:
                            continue
                        ISBN_number, book_title, price, author, available_number, publisher, genre = result
                        publisher_object = Publisher.get_publisher_object(
                            publisher)
                        if publisher_object == None:
                            print(f"Can't find {publisher} publisher,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        genre_object = Genre.get_genre_object(genre)
                        if genre_object == None:
                            print(f"Can't find {genre} genre,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        Book(
                            ISBN_number,
                            author,
                            book_title,
                            price,
                            available_number,
                            publisher_object,
                            genre_object
                        ).add()
                        

                    else:
                        continue

                elif user_input == '3':
                    system("clear")
                    data = Magazine.show_all_magazine()
                    print(print_table(data, magazine_header))
                    add_magazine = input(
                        "1: Add Magazine \n2: Back\n\n").strip()
                    if add_magazine == '1':
                        system("clear")
                        data = Publisher.show_all_publisher()
                        print(print_table(data, publisher_header))
                        print("\n")
                        data = Genre.show_all_genre()
                        print(print_table(data, genre_header))
                        result = magazine_add_choice()
                        if result == None:
                            continue
                        ISSN_number, magazine_title, price, editor, available_number, publisher, genre = result
                        publisher_object = Publisher.get_publisher_object(
                            publisher)
                        genre_object = Genre.get_genre_object(genre)
                        if publisher_object == None:
                            print(f"Can't find {publisher} publisher,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        genre_object = Genre.get_genre_object(genre)
                        if genre_object == None:
                            print(f"Can't find {genre} genre,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        Magazine(issn_number=ISSN_number,
                                      magazine_title=magazine_title,
                                      price=price,
                                      editor=editor,
                                      available_number=available_number,
                                      publication=publisher_object,
                                      genre=genre_object).add()
                    else:
                        continue

                elif user_input == '4':
                    system('clear')
                    data = Genre.show_all_genre()
                    print(print_table(data, genre_header))
                    user_genre_choice = genre_view_choice()
                    if user_genre_choice == None:
                        continue
                    else:
                        name = user_genre_choice
                        Genre(name).add()

                elif user_input == '5':
                    system("clear")
                    data = Publisher.show_all_publisher()
                    print(print_table(data, publisher_header))
                    user_publication_choice = publication_view_choice()
                    if user_publication_choice == None:
                        continue
                    else:
                        name, address, phone_number = user_publication_choice
                        Publisher(name, address, phone_number).add()

                elif user_input == '6':
                    break
        else:

            print(f"Cant verify your email or password, please login again \
Redirecting you to main menu")

            login_attempt -= 1
            print(f"{login_attempt} attempt remaning")
            if login_attempt <= 0:
                exit("To many login attempt, exiting the app.")
            sleep(2)

elif user_input == '2':
    exit()
