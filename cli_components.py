from os import system
from tabulate import tabulate
import shutil

columns = shutil.get_terminal_size().columns


def try_convert_to_int(message):
    while True:
        try:
            output = int(input(f"{message}"))
            break
        except ValueError:
            print_center("Can't converted the entered input to number please try again.")
    return output

def print_center(message):
    print(message.center(columns))

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
    print_center("                    `---`                                  \n")

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
    return input("\nEnter your choice: ")


def librarian_view_choice(librarian_name):
    system("clear")
    print_center(f"Login Sucessful, welcome {librarian_name}\n\n")
    print_center("Select option")
    print_center("\n\t 0. Show All Members")
    print_center("1. Members Options")
    print_center("2. Book Options")
    print_center("3. Magazine Options")
    print_center("4. Genre Options")
    print_center("5. Publication Options")
    print_center("6. Back")
    return input("\nEnter your choice: ")

def member_view_choice(user_object):
    system("clear")
    print_center(f"Login Sucessful, welcome {user_object.username}\n\n")
    print_center("Select option")
    print_center(" 1. Issue Book")
    print_center(" 2. Issue Magazine")
    print_center(" 3. Return Book")
    print_center(" 4. Return Magazine")
    print_center(" 5. Show all issued books and magazine")
    print_center(" 6. Back")
    return input("\nEnter your choice: ")

def book_add_choice():
    print_center("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin\n\n\n")
    
    ISBN_number = input("\nEnter the ISBN Number of book: ")
    book_title = input("\nEnter Book Title: ")
    price = try_convert_to_int("Enter the price of book: ")
    author = input("\nEnter the Author name: ")
    available_number = try_convert_to_int("Enter the number of books available: ")
    publisher = input("\nEnter the publisher's Name from table above: ")
    genre = input("\nEnter The genre name from above table: ")
    return (ISBN_number, book_title,price,author,available_number,publisher, genre)
    
    
def genre_view_choice():
    add_genre = input("\n1: Add Genre \n2: Back\n\n")
    if add_genre == '1':
        name = input("\nEnter the name of the Genre: ")
        return name
    elif add_genre == '2':
        return None

def magazine_add_choice():
    print_center("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin")
    print('\n\n')

    ISSN_number = input("\nEnter the ISSN Number of Magazine: ")
    magazine_title = input("\nEnter Magazine Title: ")
    price = try_convert_to_int("Enter the price of Magazine: ")
    editor = input("\nEnter the Author name: ")
    available_number = try_convert_to_int("Enter the number of magazine available: ")
    
    publisher = input("\nEnter the publisher's Name from table above: ")
    genre = input("\nEnter The genre name from above table: ")
    return (ISSN_number, magazine_title,price,editor,available_number,publisher, genre)

def publication_view_choice():
    add_publication = input("\n1: Add Publication \n2: Back\n\n")
    if add_publication == '1':
        name = input("\nEnter the name of the publication: ")
        address = input("\nEnter the publication's address: ")
        phone_number = input("\nEnter the publication's number: ")
        return name,address,phone_number
    elif add_publication == '2':
        return None

def add_member_menu():
    system("clear")
    username = input("\nEnter the username of the member: ")
    email = input("\nEnter the member's email: ")
    address = input("\nEnter the user's address: ")
    phone_number = input("\nEnter the user's number: ")
    return username,email,address,phone_number

def print_table(data_row,header):
    return tabulate(tabular_data=data_row, headers=header, tablefmt='fancy_grid')

def add_book_menu():
    username = input("\nEnter the username of the member: ")
    email = input("\nEnter the member's email: ")
    address = input("\nEnter the user's address: ")
    phone_number = input("\nEnter the user's number: ")
    return username,email,address,phone_number

def issue_book_menu():
    ISBN_to_issue = input("\nEnter the ISBN number of the book you want: ")
    days= input("\nDo you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days=='y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISBN_to_issue, days_to_add    

def return_book_menu():
    return input("\nEnter the ISBN number of the book you want: ")

def issue_magazine_menu():
    ISSN_to_issue = input("\nEnter the ISSN number of the magazine you want to return: ")
    days= input("\nDo you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days=='y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISSN_to_issue, days_to_add  
    
def return_magazine_menu():
    return input("\nEnter the ISSN number of the magazine you want to return: ")





