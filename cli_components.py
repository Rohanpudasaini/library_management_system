from os import system
from tabulate import tabulate
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
    return input("\nEnter your coice: ")

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
    return input("\nEnter your coice: ")

def book_view_choice():
    system("clear\n\n")
    print("Select option")
    print("\n\t 1. Add Book")
    print("\t 2. Remove Book")
    print("\t 3. Back")
    return input("\nEnter your coice: ")
    
def genre_view_choice():
    # system("clear\n\n")
    # print("Select option")
    # print("\n\t 1. Add Genre")
    # print("\t 2. Edit Genre")
    # print("\t 3. Remove Genre")
    # print("\t 4. Back")
    # return input("\nEnter your coice: ")
    add_publication = input("1: Add Genre \n2: Back\n\n")
    if add_publication == '1':
        name = input("Enter the name of the Genre: ")
        return name
    elif add_publication == '2':
        return None

def magazine_view_choice():
    system("clear\n\n")
    print("Select option")
    print("\n\t 1. Add Magazine")
    print("\t 2. Remove Magazine")
    print("\t 3. Back")
    return input("\nEnter your coice: ")

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



