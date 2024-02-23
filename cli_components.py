from os import system
from tabulate import tabulate
import shutil

columns = shutil.get_terminal_size().columns


def try_convert_to_int(message):
    while True:
        try:
            output = int(input(f"{message}").strip())
            break
        except ValueError:
            print_center(
                "Can't converted the entered input to number please try again.")
    return output


def print_center(message):
    print(message.center(columns))


def validate_length_and_digit(name:str, without=None, length=None ):
    tried = 5 
    while True:
        returning_name = input_strip(
                f"\nEnter the {name}  without {without}: ")
        if len(str(returning_name)) == length and str(returning_name).isdigit():
            return returning_name
        elif not str(returning_name).isdigit():
            print(f"Make sure the input contain the digit only")
        elif len(returning_name) != length:
            print(f"Please make sure the input is {length} long")
        tried -= 1
        print(f"You got {tried} try remaning" )
        if tried ==0:
            return None
        


def input_strip(message):
    return input(message).strip()


def assci_art():
    # Art by Donovan Bake

    system('clear')
    print('\n\n')
    print_center("      __...--~~~~~-._   _.-~~~~~--...__                    ")
    print_center("    //               `V'               \\                  ")
    print_center("   //                 |                 \\                 ")
    print_center("  //__...--~~~~~~-._  |  _.-~~~~~~--...__\\                ")
    print_center(" //__.....----~~~~._\ | /_.~~~~----.....__\\               ")
    print_center("====================\\|//====================              ")
    print_center(
        "                    `---`                                  \n")

    print_center("   ____                __    _ __                          ")
    print_center("  / __ \__  _______   / /   (_) /_  _________ ________  __ ")
    print_center(" / / / / / / / ___/  / /   / / __ \/ ___/ __ `/ ___/ / / / ")
    print_center("/ /_/ / /_/ / /     / /___/ / /_/ / /  / /_/ / /  / /_/ /  ")
    print_center("\____/\__,_/_/     /_____/_/_.___/_/   \__,_/_/   \__, /   ")
    print_center("                                                 /____/    ")
    input("Press any key to continue.")

# assci_art()


def main_menu_choice():

    print_center("Welcome to our Library")
    print_center("Please select what you want to do.")
    print("\n")
    print_center("1: Librarian Login")
    print_center("2: Exit")
    return input_strip("\nEnter your choice: ")


def librarian_view_choice(librarian_name):
    system("clear")
    print_center(f"Login Sucessful, welcome {librarian_name}\n\n")
    print_center("Select option")
    print_center("0. Show All Members")
    print_center("1. Members Options")
    print_center("2. Book Options")
    print_center("3. Magazine Options")
    print_center("4. Genre Options")
    print_center("5. Publication Options")
    print_center("6. Back")
    return input_strip("\nEnter your choice: ")


def member_view_choice(username):
    system("clear")
    print_center(f"Login Sucessful, welcome {username}\n\n")
    print_center("Select option")
    print_center(" 1. Issue Book")
    print_center(" 2. Issue Magazine")
    print_center(" 3. Return Book")
    print_center(" 4. Return Magazine")
    print_center(" 5. Show all issued books and magazine")
    print_center(" 6. Back")
    return input_strip("\nEnter your choice: ")


def book_add_choice():
    print_center("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin\n\n\n")

    ISBN_number = validate_length_and_digit('ISBN number', "- or spaces", 13)
    if book_add_choice == None:
        return None
    book_title = input_strip("\nEnter Book Title: ")
    price = try_convert_to_int("Enter the price of book: ")
    author = input_strip("\nEnter the Author name: ")
    available_number = try_convert_to_int(
        "Enter the number of books available: ")
    publisher = try_convert_to_int("\nEnter the publisher's ID from table above: ")
    genre = try_convert_to_int("\nEnter The genre ID from above table: ")
    return (ISBN_number, book_title, price, author, available_number, publisher, genre)


def genre_view_choice():
    add_genre = input_strip("\n1: Add Genre \n2: Back\n\n")
    if add_genre == '1':
        name = input_strip("\nEnter the name of the Genre: ")
        if name == '':
            print("The name can't be empty, please try again")
            input("Press any key to continue")
            return None
        return name
    elif add_genre == '2':
        return None


def magazine_add_choice():
    print_center("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin")
    print('\n\n')

    # ISSN_number = input("\nEnter the ISSN Number of Magazine: ")
    ISSN_number = validate_length_and_digit('ISSN number', "- or spaces", 8)
    if ISSN_number ==None: return None
    magazine_title = input_strip("\nEnter Magazine Title: ")
    price = try_convert_to_int("Enter the price of Magazine: ")
    editor = input_strip("\nEnter the Author name: ")
    available_number = try_convert_to_int(
        "Enter the number of magazine available: ")

    publisher = try_convert_to_int("\nEnter the publisher's ID from table above: ")
    # genre = input_strip("\nEnter The genre ID from above table: ")
    genre = try_convert_to_int("\nEnter The genre ID from above table: ")
    return (ISSN_number, magazine_title, price, editor, available_number, publisher, genre)


def publication_view_choice():
    add_publication = input_strip("\n1: Add Publication \n2: Back\n\n")
    if add_publication == '1':
        name = input_strip("\nEnter the name of the publication: ")
        address = input_strip("\nEnter the publication's address: ")
        # phone_number = input("\nEnter the publication's number: ")
        phone_number = validate_length_and_digit(name="Phone Number", without="country code", length=10)
        if name == '' or address == '' or phone_number == '':
            input("All fields are required, please try again.\n\
\n\nPress any key to continue")
            return None
        return name, address, phone_number
    elif add_publication == '2':
        return None


def add_member_menu():
    system("clear")
    username = input_strip("\nEnter the username of the member: ")
    email = input_strip("\nEnter the member's email: ")
    address = input_strip("\nEnter the user's address: ")
    phone_number = validate_length_and_digit(name="Phone number", without= "country code", length=10)
    return username, email, address, phone_number


def print_table(data_row, header):
    return tabulate(
        tabular_data=data_row, 
        headers=header, 
        tablefmt='fancy_grid',  
        maxcolwidths=[None, None, 40]
        )


def issue_book_menu():
    # ISBN_to_issue = input("\nEnter the ISBN number of the book you want: ")
    ISBN_to_issue = validate_length_and_digit(
        name="ISBN number to issue book", without="'-' or spaces", length=13)
    if ISBN_to_issue ==None: return None
    days = input_strip(
        "\nDo you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days == 'y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISBN_to_issue, days_to_add


def return_book_menu():
    ISBN_to_return  = validate_length_and_digit(name="ISBN number of the book to return", without="'-' or spaces", length=13)
    return ISBN_to_return


def issue_magazine_menu():
    # ISSN_to_issue = str(try_convert_to_int(input_strip(
        # "\nEnter the ISSN number of the magazine you want to return: ")))
    # try_convert_to_int(ISSN_to_issue)
    ISSN_to_issue = validate_length_and_digit(name = "ISSN number of the magazine you want to Issue", without="'-' or spaces", length=8)
    if ISSN_to_issue == None: return None
    days = input_strip(
        "\nDo you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days == 'y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISSN_to_issue, days_to_add


def return_magazine_menu():
    ISSN_to_return = validate_length_and_digit(name = "ISSN number of the magazine you want to return", without="'-' or spaces", length=8)
    return ISSN_to_return    


def show_fine_menu(username):
    print("\n\n")
    print_center(f"Hello {username}, you have some fine remaning!!")
    print_center("please contact account department")
    print_center("And return the books with fine")
    print("\n\n")
    input_strip("Press any key to continue")


def error_assci():
    system("clear")
    print('\n\n')
    print_center("    Database Error              |     |     ")
    print_center("                                \\_V_//     ")
    print_center("                                \/=|=\/     ")
    print_center("                                 [=v=]      ")
    print_center("                               __\___/_____ ")
    print_center("                              /..[  _____  ]")
    print_center("                             /_  [ [  M /] ]")
    print_center("                            /../.[ [ M /@] ]")
    print_center("                           <-->[_[ [M /@/] ]")
    print_center("                          /../ [.[ [ /@/ ] ]")
    print_center("     _________________]\ /__/  [_[ [/@/ C] ]")
    print_center("    <_________________>>0---]  [=\ \@/ C / /")
    print_center("       ___      ___   ]/000o   /__\ \ C / / ")
    print_center("          \    /              /....\ \_/ /  ")
    print_center("       ....\||/....           [___/=\___/   ")
    print_center("      .    .  .    .          [...] [...]   ")
    print_center("     .      ..      .         [___/ \___]   ")
    print_center("     .    0 .. 0    .         <---> <--->   ")
    print_center("  /\/\.    .  .    ./\/\      [..]   [..]   ")
    print_center(" / / / .../|  |\... \ \ \    _[__]   [__]_  ")
    print_center("/ / /       \/       \ \ \  [____>   <____] ")
