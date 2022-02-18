import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import csv
import logging

class mysqlOperations:

    """ This class is created to demonstate various mysql operations in python """



    def __init__(self,dbname):
        self.dbname=dbname
        self.my_connection = None
        logging.basicConfig(filename="demo.log", level=logging.ERROR)
        try:

            self.my_connection = connection.MySQLConnection(user='dhoni', password='Welcome@123', host='127.0.0.1',
                                               database="python")
            self.mycursor = self.my_connection.cursor()
            print("Connection Established successfully ! ")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
                logging.error(err)
            else:
                logging.error(err)

    def create_table(self):
        try:
            while True:
                table_name=input("Enter the table name to create : ")
                # print(table_name)
                # print(type(table_name))
                query="""SHOW TABLES"""
                self.mycursor.execute(query)
                data = self.mycursor.fetchall()
                # print(data)
                # print(type(data))
                for i in data:

                    str_i = ''.join(i)
                    # print(str_i)
                    # print(type(str_i))
                    if str_i == table_name:
                        choice=input(("Sorry !! Table  already exists in the database , do you want to create table with new name ? y/n \n"))
                        break
                    else:
                        continue
                else:

                    query = """CREATE TABLE  {} (student_id int PRIMARY KEY, student_name VARCHAR(20) NOT NULL,student_address VARCHAR(100))""".format(
                        table_name)
                    self.mycursor.execute(query)
                    print("Table created ")
                    choice=""

                if choice.upper() == "Y":
                    continue
                elif choice.upper() == "N":
                    print("Table creation operation is terminated by the user !!")
                    break
                else:
                    break

        except Exception as e:
            logging.error("Error occured during table creation")
            logging.error(e)

    def insert_table(self):
        try:
            table_name=input("Enter the table name to insert values :")
            query1="""SELECT * FROM {}""".format(table_name)
            self.mycursor.execute(query1)
            data = self.mycursor.fetchall()
            num_fields = len(self.mycursor.description)
            print(num_fields)
            columns_name= [i[0] for i in self.mycursor.description]
            print(columns_name)
            print(type(columns_name))
            print("--------------------------------------")
            queryBase = "INSERT INTO {} values (%s)".format(table_name)
            final_query=queryBase % ",".join('%s' for i in range(0, num_fields))

            user_choice=int(input("Please select the  input method : \n 1. csv file \n 2. user input \n"))
            if user_choice == 1:
                root = tkinter.Tk()
                root.withdraw()
                tkinter.messagebox.showinfo("File ","Please select the file containing data")
                input_file = filedialog.askopenfilename()

                # query = "INSERT INTO {} values (%s,%s,%s)".format(table_name)
                with open(input_file,'r') as fin:
                    csvfile = csv.reader(fin, delimiter=",")
                    headings = next(csvfile)
                    all_value=[]
                    for row in csvfile:
                        # print(row)
                        self.mycursor.execute(final_query,row)
                #         value=(row[0],row[1],row[2])
                #         all_value.append(value)
                # self.mycursor.executemany(final_query,all_value)
                print("Values inserted into the table successfully!!")
                # query="""INSERT INTO {} (student_id,student_name,student_address) VALUES (102,"virat","Delhi")""".format(table_name)
                # self.mycursor.execute(query)
                self.print_data(table_name)
            elif user_choice == 2:
                print("Manual input ")
                all_value = []
                tup = ()
                for i in range(len(columns_name)):
                    value=input("Enter value for {}: ".format(columns_name[i]))
                    tup = tup + (value,)
                all_value.append(tup)
                # print(all_value)
                self.mycursor.executemany(final_query,all_value)
                print("Value inserted to the table successfully !!")
                self.print_data(table_name)
            else:
                logging.error("Invalid user input")

        except Exception as e:
            logging.error("Error occured during inserting data into table")
            logging.error(e)

    def print_data(self,table):
        try:
            query = """SELECT * FROM {}""".format(table)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            print("Printing the data ......")
            for x in data:
                print(x)
        except Exception as e:
            logging.error("Error while retreiving the data ")
            logging.error(e)

    def delete_data(self):
        try:
            query=""
            input_table=input("Please enter the table name to delete : ")
            criteria=int(input("Enter the criteria to delete  :\n 1. All data \n 2.Based on a column\n"))
            if criteria == 1:
                query="""DELETE FROM {s}""".format(s=input_table)
            elif criteria == 2:
                column_name=input("Enter the column name: ")
                column_value=input("Enter the value: ")
                query = """DELETE FROM {s} WHERE {c}={v}""".format(s=input_table,c=column_name,v=column_value)
            else:
                logging.error("Invalid input, Delete operation terminated !!")

            # query = """DELETE FROM {s} WHERE student_id=100""".format(s=input_table)
            if query != "":
                self.mycursor.execute(query)
                print("Successfully deleted !!")
                self.print_data(input_table)
        except Exception as e:
            logging.error("Error occured while deleting the record")
            logging.error(e)

    # def insert_table_multi(self):
    #     query= """INSERT INTO student (id,name) VALUES (%s,%s)"""
    #     val = [
    #          (102,'Peter'),
    #         (103,'Amy'),
    #          (104,'Hannah')
    #         ]
    #     self.mycursor.executemany(query, val)

    def update_table(self):
        try:
            input_table=input("Enter the table name to update : ")
            update_condition_column=input("Enter the update condition column: ")
            update_condition_value=input("Enter the update condition column value: ")
            update_column=input("Enter the column which need to be updated : ")
            update_column_value=input("Enter the new value: ")
            # query="""UPDATE student_table SET student_name="Kohli" WHERE student_id=101"""
            query = """UPDATE {_a} SET {_b}={_c} WHERE {_d}={_e}""".format(_a=input_table,_b=update_column,_c=update_column_value,_d=update_condition_column,_e=update_condition_value)
            self.mycursor.execute(query)
            print("Table updated successfully !!")
            self.print_data(input_table)
        except Exception as e:
            logging.error("Error occured while deleting the record")
            logging.error(e)

    def commit_close(self):
        if self.my_connection != None:
            self.my_connection.commit()
            self.my_connection.close()

def main():
    try:
        dbname= input("Enter the database name : ")
        my_sql=mysqlOperations(dbname)
        if my_sql.my_connection != None:
            while True :
                operation = int(input(
                    "Please choose the db operation to be performed : \n 1. Create Table \n 2. Update Table \n 3. Insert Table \n 4. Fetch Data From Table \n 5.Delete data \n"))
                if operation == 1:
                    my_sql.create_table()
                elif operation == 2:
                    my_sql.update_table()
                elif operation == 3:
                    my_sql.insert_table()
                elif operation == 4:
                    input_table=input("Enter the table name : ")
                    my_sql.print_data(input_table)
                elif operation ==5:
                    my_sql.delete_data()
                else:
                    logging.error("Invalid Selection !!")
                choice=input("Do you want to continue with a new operation: Y/N \n ")
                if choice.upper() == "Y":
                    continue
                else:
                    break
    except Exception as e:
        logging.error(e)
    finally:
        my_sql.commit_close()

if __name__=="__main__":
    main()
