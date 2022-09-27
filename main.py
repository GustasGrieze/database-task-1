# Create Console program :
# which would ask to:
# - create database
# - create table (column names: name, surname, age, salary)
# - populate table with 50 elements (name, surname auto generated, age from 18 to 99, salary from 50 000 to 250 000 (with a step size of 25000))
# - print the names of people who earn more than entered value (in a prompt)
# - print all users (names and surnames)
# - delete user by surname
# OOP, application should be runned a module.

import sqlite3
import names
from random import randint, randrange
import time

class SqlDatabase:
    def __init__(self, db_name: str) -> None:
        self._conn = sqlite3.connect(db_name+".db")
        self._cursor = self._conn.cursor()

    def create_table(self, table_name: str, columns: str) -> None:
        try:
            with self._conn:
                self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                {table_name} (
                {columns}
                )""")
        except Exception as e:
            print(f"Unable to create table!. Error msg: {e}")

    def write(self, table_name: str, entry_values: str) -> None:
        with self._conn:
            self._cursor.execute(f"INSERT INTO {table_name} VALUES ({entry_values})")

def generate_first_name() -> str:
    return names.get_first_name()

def generate_last_name() -> str:
    return names.get_last_name()

def get_random_age() -> int:
    return randint(18, 99)

def get_random_salary() -> int:
    return randrange(50000, 250000, 25000)


class MainDatabase(SqlDatabase):
    def __init__(self) -> None:
        self.user_database_name = input("Enter your desired database name: ")
        super().__init__(self.user_database_name)
        self.user_table_name = input("Please enter your desired table name: ")
        self.user_column_names = input("Please enter your column names: ")
        self.db = SqlDatabase(self.user_database_name)
        self.create_database_table()
        self.populate_database()
        self.interface()

    def create_database_table(self) -> None:
        self.db.create_table(self.user_table_name, self.user_column_names)

    def populate_database(self) -> None:
        for i in range(500):
            self.db.write(table_name=self.user_table_name, entry_values=f"'{generate_first_name()}', '{generate_last_name()}', '{get_random_age()}', '{get_random_salary()}'")
            percent = i//5
            print(f"{percent}%", end="\rCompleted: ", flush=True)
            # self.progress(amount, i)

    def print_users_with_a_bigger_than_selected_salary(self) -> None:
        value = input("Please enter the amount of money you want: ")
        with self._conn:
            self._cursor.execute(f"SELECT Name From {self.user_table_name} WHERE Salary >= {value}")
            return (self._cursor.fetchall())

    def print_every_user(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name}")
            return (self._cursor.fetchall())

    def delete_selected_user(self) -> str:
        selected_user_surname = input("Enter the surname of the user you would like to delete: ")
        with self._conn:
            self._cursor.execute(f"DELETE from {self.user_table_name} WHERE surname={selected_user_surname}")
            return f"Deleted user {selected_user_surname}"

    def select_specified_people_1(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name} WHERE Name LIKE'a%' AND Surname LIKE'%w%'")
            return (self._cursor.fetchall())

    def select_specified_people_2(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name} WHERE Salary < 150000 OR Age > 50")
            return (self._cursor.fetchall())

    def select_specified_people_3(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname, Salary FROM {self.user_table_name} WHERE Age BETWEEN 38 AND 72")
            return (self._cursor.fetchall())

    def select_specified_people_4(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT COUNT(Name), AVG(Salary) FROM {self.user_table_name} WHERE Age BETWEEN 19 AND 43")
            return (self._cursor.fetchall())

    def interface(self) -> None:
        while True:
            time.sleep(3)
            first_input = input('''\n
            Welcome to our HR system
            Select one of the options bellow to choose which operation you would like to execute:
            1 - Print every user in the database
            2 - Delete a user from the database
            3 - Print users with a bigger than selected salary
            4 - Specialized command
            5 - Specialized command
            6 - Specialized command
            7 - Specialized command

            To exit the program, type EXIT.
            
            Your choice: \n''').lower()
                
            if first_input == '1':
                print(self.print_every_user())

            elif first_input == '2':
                print(self.delete_selected_user())

            elif first_input == '3':
                print(self.print_users_with_a_bigger_than_selected_salary())

            elif first_input == '4':
                print(self.select_specified_people_1())

            elif first_input == '5':
                print(self.select_specified_people_2())

            elif first_input == '6':
                print(self.select_specified_people_3())

            elif first_input == '7':
                print(self.select_specified_people_4())

            elif first_input == 'exit':
                print("The program has ended")
                break

            else:
                print("You need to choose between 1 - 11 ")


if __name__ == "__main__":
    MainDatabase()