# Library Management System

This is a simple CLI based library management system made using python and PostgreSql for databse and SQLAlchemy for ORM.
It incooperate some of the knowledge of OOP and SQLAlchemy.

## SQLAlchemy

SqlAlchemy is an ORM which is used to represent out databse(Postgres in this case) as objects and classes. SqlAlchemy not only provide the ORM but can also be used as a query builder.

### How to Run

1. Clone the repo.

    ```bash
    git clone https://github.com/Rohanpudasaini/library_management_system/tree/master
    ```

2. Move to the folder

    ```bash
    cd library_management_system
    ```

3. Mov to the databse_connection folder

    ```bash
    cd databse_connection
    touch .env
    ```

4. Make your .env file

    The env file must be something like this, please change it according to your database's information.

    ```bash
    host=hostaddress
    database=databse
    user=username
    password=password
    ```

5. Move back to the main folder and run the app

    Run the cli app by running `python3 libraryWizard.py`.

Enjoy
