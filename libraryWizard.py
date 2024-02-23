# from getpass import getpass
from pwinput import pwinput
from os import system
from databse_connection.db_handler import MagazineClass, Members, Book, Library_Admin, \
    Publications, GenreClass
from cli_components import assci_art, issue_book_menu, issue_magazine_menu, librarian_view_choice, \
    main_menu_choice, member_view_choice, book_add_choice, \
    genre_view_choice, magazine_add_choice, add_member_menu, print_center, print_table, \
    publication_view_choice, return_book_menu, return_magazine_menu, columns, show_fine_menu
from time import sleep
logged_in = False
# while True:

assci_art()
user_input = main_menu_choice()
if user_input == '1':
    login_attempt = 5
    while True:

        if not logged_in:
            email = input("Enter your Email: ").strip()
            password = pwinput("Enter your Passkey: ", mask="*")
            login_sucess, librarian_name = Library_Admin.librarian_login(
                email=email, password=password)

        if login_sucess:
            logged_in = True
            while True:
                user_input = librarian_view_choice(librarian_name)
                if user_input == '0':
                    data, header = Members.show_all_members()
                    print(print_table(data_row=data, header=header))
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
                            Members(username, email, address, phone_number)

                        elif add_member == '2':
                            select_member = input(
                                "Enter the username of the member: ").strip()
                            member_present, user_object = Members.is_member(
                                select_member)
                            if not member_present:

                                print("No member with that username please check once again\
                                    \nRedirecting to home page")
                                sleep(1.5)
                                continue

                            else:
                                Members.calculate_fine(user_object)
                                if user_object.fine > 0:
                                    show_fine_menu(user_object.username)
                                    # Members.pay_fine(user_object.fine, columns)
                                    # user_object.fine = 0
                                while True:
                                    user_member_choice = member_view_choice(
                                        user_object.username)
                                    if user_member_choice == '1':
                                        system("clear")
                                        data, header = Book.show_all_book()
                                        print('\n')
                                        print_center("All Available Book")
                                        print('\n')
                                        print(print_table(data, header))
                                        result = issue_book_menu()
                                        if result == None: continue
                                        ISBN_number_to_issue, days_to_issue = result
                                        Members.member_add_book(
                                            select_member,
                                            ISBN_number_to_issue,
                                            days_to_issue)

                                    elif user_member_choice == '2':
                                        system('clear')
                                        data, header = MagazineClass.show_all_magazine()
                                        print('\n')
                                        print_center("All Available Magazine")
                                        print('\n')
                                        print(print_table(data, header))
                                        result = issue_magazine_menu()
                                        if result == None: continue
                                        ISSN_number_to_issue, days_to_issue= result
                                        Members.member_add_magazine(
                                            select_member,
                                            ISSN_number_to_issue,
                                            days_to_issue
                                        )

                                    elif user_member_choice == '3':
                                        system('clear')
                                        data, header = Members.show_all_members()
                                        print(print_table(
                                            data_row=data, header=header))
                                        data, header = Book.show_all_book()
                                        print(print_table(data, header))
                                        ISBN_number_to_return = return_book_menu()
                                        if ISBN_number_to_return == None: continue
                                        Members.member_return_book(
                                            select_member,
                                            ISBN_number_to_return
                                        )

                                    elif user_member_choice == '4':
                                        system('clear')
                                        data, header = Members.show_all_members()
                                        print(print_table(
                                            data_row=data, header=header))
                                        data, header = MagazineClass.show_all_magazine()
                                        print(print_table(data, header))
                                        ISSN_number_to_return = return_magazine_menu()
                                        if ISSN_number_to_return == None: continue
                                        Members.member_return_magazine(
                                            select_member,
                                            ISSN_number_to_return
                                        )

                                    elif user_member_choice == '5':
                                        system('clear')
                                        print("\n\nAll Book")
                                        data, header = Book.show_users_all_book(
                                            user_object)
                                        print(print_table(data, header))
                                        print("\n\nAll Magazine")
                                        data, header = MagazineClass.show_users_all_magazine(
                                            user_object)
                                        print(print_table(data, header))

                                        input("Enter Any key to continue")

                                    else:
                                        break
                        else:
                            break

                elif user_input == '2':
                    system("clear")
                    data, header = Book.show_all_book()
                    print(print_table(data, header))
                    add_book = input("1: Add Book \n2: Back\n\n").strip()

                    if add_book == '1':
                        system("clear")
                        data, header = Publications.show_all_publisher()
                        print(print_table(data, header))
                        print("\n")
                        data, header = GenreClass.show_all_genre()
                        print(print_table(data, header))
                        result = book_add_choice()
                        if result == None: continue
                        ISBN_number, book_title, price, author, available_number, publisher, genre = result
                        publisher_object = Publications.get_publisher_object(
                            publisher)
                        if publisher_object == None:
                            print(f"Can't find {publisher} publisher,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        genre_object = GenreClass.get_genre_object(genre)
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
                        )

                    else:
                        continue

                elif user_input == '3':
                    system("clear")
                    data, header = MagazineClass.show_all_magazine()
                    print(print_table(data, header))
                    add_magazine = input(
                        "1: Add Magazine \n2: Back\n\n").strip()
                    if add_magazine == '1':
                        system("clear")
                        data, header = Publications.show_all_publisher()
                        print(print_table(data, header))
                        print("\n")
                        data, header = GenreClass.show_all_genre()
                        print(print_table(data, header))
                        result = magazine_add_choice()
                        if result == None: continue
                        ISSN_number, magazine_title, price, editor, available_number, publisher, genre = result
                        publisher_object = Publications.get_publisher_object(
                            publisher)
                        genre_object = GenreClass.get_genre_object(genre)
                        if publisher_object == None:
                            print(f"Can't find {publisher} publisher,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        genre_object = GenreClass.get_genre_object(genre)
                        if genre_object == None:
                            print(f"Can't find {genre} genre,")
                            print("please check if it exsist or not in our system")
                            print("redirecting back, please wait")
                            sleep(3.5)
                            continue

                        MagazineClass(ISSN_number=ISSN_number,
                                      magazine_title=magazine_title,
                                      price=price,
                                      editor=editor,
                                      available_number=available_number,
                                      publication=publisher_object,
                                      genre=genre_object)
                    else:
                        continue

                elif user_input == '4':
                    system('clear')
                    data, header = GenreClass.show_all_genre()
                    print(print_table(data, header))
                    user_genre_choice = genre_view_choice()
                    if user_genre_choice == None:
                        continue
                    else:
                        name = user_genre_choice
                        GenreClass(name)

                elif user_input == '5':
                    system("clear")
                    data, header = Publications.show_all_publisher()
                    print(print_table(data, header))
                    user_publication_choice = publication_view_choice()
                    if user_publication_choice == None:
                        continue
                    else:
                        name, address, phone_number = user_publication_choice
                        Publications(name, address, phone_number)

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
