# from getpass import getpass
from pwinput import pwinput
from os import system
from databse_connection.db_handler import Members, Book, Library_Admin, Publications, GenreClass
from cli_components import librarian_view_choice, member_view_choice, book_view_choice, \
    genre_view_choice, magazine_view_choice, add_member_menu, print_table, publication_view_choice
from time import sleep
logged_in = False
while True:

    system('clear')
    print("Welcome to our Library")
    print("Please select what you want to do.")
    print("\n1: Librarian Login\
        \n2: Exit")
    user_input = input("\nEnter your choice: ")

    if user_input == '1':
        if not logged_in:
            email = input("Enter your Email: ")
            password = pwinput("Enter your Passkey: ", mask="*")
            login_sucess, librarian_name = Library_Admin.librarian_login(
                email=email, password=password)
            

        if login_sucess:
            logged_in = True
            user_input = librarian_view_choice(librarian_name)
            if user_input == '0':
                data , header = Members.show_all_members()
                print(print_table(data_row=data,header=header))
                input("\n\n Press any key to go back to menu")
            if user_input == '1':
                add_member = input("\n1. Add New Member \n2. Select Old Member\
                    \n\nEnter your choice:")

                if add_member == '1':
                    username, email, address, phone_number = add_member_menu()
                    Members(username, email, address, phone_number)

                elif add_member == '2':
                    select_member = input("Enter the username of the member: ")
                    member_present, user_object = Members.is_member(
                        select_member)
                    if not member_present:

                        print("No member with that username please check once again\
                            \nRedirecting to home page")
                        sleep(1.5)
                        continue

                    else:

                        user_member_choice = member_view_choice(user_object)
                        

            elif user_input == '2':

                user_book_choice = book_view_choice()
                
                if user_book_choice == '1':
                    system("clear")
                    

            elif user_input == '3':

                user_magazine_choice = magazine_view_choice()

            elif user_input == '4':
                system('clear')
                data,header = GenreClass.show_all_genre()
                print(print_table(data,header))
                user_genre_choice = genre_view_choice()
                if user_genre_choice == None:
                    continue
                else:
                    name = user_genre_choice
                    GenreClass(name)
            
            elif user_input == '5':
                system("clear")
                data, header = Publications.show_all_publisher()
                print(print_table(data,header))
                user_publication_choice = publication_view_choice()
                if user_publication_choice == None:
                    continue
                else:
                    name,address,phone_number = user_publication_choice
                    Publications(name,address,phone_number)
                

        else:

            print(f"Cant verify your email or password, please login again\
                \nRedirecting you to main menu")
            sleep(2)

    elif user_input == '2':

        break
