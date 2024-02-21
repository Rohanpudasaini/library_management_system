from os import system
from tabulate import tabulate


def try_convert_to_int(message):
    while True:
        try:
            output = int(input(f"{message}"))
            break
        except ValueError:
            print("Can't converted the entered input to number please try again.")
    return output

def librarian_view_choice(librarian_name):
    system("clear")
    print(f"Login Sucessful, welcome {librarian_name}\n\n")
    print("Select option")
    print("\n\t 0. Show All Members")
    print("\t 1. Members Options")
    print("\t 2. Book Options")
    print("\t 3. Magazine Options")
    print("\t 4. Genre Options")
    print("\t 5. Publication Options")
    print("\t 6. Back")
    return input("\nEnter your choice: ")

def member_view_choice(user_object):
    system("clear")
    print(f"Login Sucessful, welcome {user_object.username}\n\n")
    print("Select option")
    print("\n\t 1. Issue Book")
    print("\t 2. Issue Magazine")
    print("\t 3. Return Book")
    print("\t 4. Return Magazine")
    print("\t 5. Show all issued books and magazine")
    print("\t 6. Back")
    return input("\nEnter your choice: ")

def book_add_choice():
    print("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin\n\n\n")
    # book3 = Books(ISBN_number='1234567891013', author='Rohan', book_title='Very Good Book3',
                    #   price=1000, available_number=10, publisher=publisher1, genre=genre3)
    ISBN_number = input("Enter the ISBN Number of book: ")
    book_title = input("Enter Book Title: ")
    price = try_convert_to_int("Enter the price of book: ")
    author = input("Enter the Author name: ")
    available_number = try_convert_to_int("Enter the number of books available: ")
    publisher = input("Enter the publisher's Name from table above: ")
    genre = input("Enter The genre name from above table: ")
    return (ISBN_number, book_title,price,author,available_number,publisher, genre)
    
    
def genre_view_choice():
    add_genre = input("1: Add Genre \n2: Back\n\n")
    if add_genre == '1':
        name = input("Enter the name of the Genre: ")
        return name
    elif add_genre == '2':
        return None

def magazine_add_choice():
    print("If you don't find your required publisher or genre, please add it\
 from main menu or ask admin\n\n\n")

    ISSN_number = input("Enter the ISSN Number of Magazine: ")
    magazine_title = input("Enter Magazine Title: ")
    price = try_convert_to_int("Enter the price of Magazine: ")
    editor = input("Enter the Author name: ")
    available_number = try_convert_to_int("Enter the number of magazine available: ")
    
    publisher = input("Enter the publisher's Name from table above: ")
    genre = input("Enter The genre name from above table: ")
    return (ISSN_number, magazine_title,price,editor,available_number,publisher, genre)

def publication_view_choice():
    add_publication = input("1: Add Publication \n2: Back\n\n")
    if add_publication == '1':
        name = input("Enter the name of the publication: ")
        address = input("Enter the publication's address: ")
        phone_number = input("Enter the publication's number: ")
        return name,address,phone_number
    elif add_publication == '2':
        return None

def add_member_menu():
    system("clear")
    username = input("Enter the username of the member: ")
    email = input("Enter the member's email: ")
    address = input("Enter the user's address: ")
    phone_number = input("Enter the user's number: ")
    return username,email,address,phone_number

def print_table(data_row,header):
    return tabulate(tabular_data=data_row, headers=header, tablefmt='fancy_grid')

def add_book_menu():
    username = input("Enter the username of the member: ")
    email = input("Enter the member's email: ")
    address = input("Enter the user's address: ")
    phone_number = input("Enter the user's number: ")
    return username,email,address,phone_number

def issue_book_menu():
    ISBN_to_issue = input("Enter the ISBN number of the book you want: ")
    days= input("Do you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days=='y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISBN_to_issue, days_to_add    

def return_book_menu():
    return input("Enter the ISBN number of the book you want: ")

def issue_magazine_menu():
    ISSN_to_issue = input("Enter the ISSN number of the magazine you want to return: ")
    days= input("Do you want to take this book for more than 15 days (y/n): ").lower()
    days_to_add = 15
    if days=='y':
        days_to_add = try_convert_to_int("Enter the days you want to borrow the book for \
            (eg 1 ,2)")
    return ISSN_to_issue, days_to_add  
    
def return_magazine_menu():
    return input("Enter the ISSN number of the magazine you want to return: ")





