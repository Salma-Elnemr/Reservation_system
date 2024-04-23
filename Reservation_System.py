import tkinter as tk
# import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Button
from tkinter import messagebox
# from tkinter_input_box.input_box import InputBox
import sqlite3
import re
from tkcalendar import DateEntry
import pandas as pd

# creating the db
conn = sqlite3.connect("reservation_system.db")

# creating the tables
# creating the Customer table.

sql_create_customer_table = """CREATE TABLE IF NOT EXISTS Customers (
                                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    customer_name TEXT NOT NULL,
                                    phone_number TEXT NOT NULL,
                                    email_address TEXT NOT NULL
                                    ); """  # Customer table
c = conn.cursor()
c.execute(sql_create_customer_table)

# creating the TableSeating table.

sql_create_tableseating_table = """CREATE TABLE IF NOT EXISTS TableSeating (
                                        table_num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        capacity INTEGER NOT NULL
                                        ); """  # TableSeating table
c = conn.cursor()
c.execute(sql_create_tableseating_table)

# creating Reservation table.
# "customer_id" is a foreign key, referencing the "Customer" table.
# "table_id" is a foreign key, referencing the "TableSeating" table.

sql_create_reservation_table = """CREATE TABLE IF NOT EXISTS Reservations (
                                        reservation_id INTEGER PRIMARY KEY,
                                        reservation_date TEXT NOT NULL,
                                        cust_id REFERENCES Customers(customer_id),
                                        table_no REFERENCES TableSeating(table_num)
                                        ); """
c = conn.cursor()
c.execute(sql_create_reservation_table)  # reservations table


# def insrt_tables():
#     conn = sqlite3.connect('reservation_system.db')
#     cursor = conn.cursor()
#     table_Data = [(1, 2),
#                   (2, 3),
#                   (3, 4),
#                   (4, 5),
#                   (5, 6),
#                   (6, 7)
#                   ]
#     cursor.executemany('INSERT OR IGNORE INTO TableSeating(table_num, capacity) VALUES (?, ?)', table_Data)



#
def get_tables():
    conn = sqlite3.connect("reservation_system.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TableSeating')
    tables = cursor.fetchall()
    conn.close()
    return tables


class RestaurantBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Booking System")

        # login functionality.
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        # Username and Password entry fields
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login button
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        # Validate the username and password.
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        #
        # # TODO: Implement actual validation logic (compare against database)
        # we could make the below if statement the "master login", and after adding a new customer we can check it agaisnt the db.
        # if username == "admin" and password == "password":
        if self.username_entry.get() == 'admin' and self.password_entry.get() == 'password':
            # Successful login, destroy login frame and load the main window
            self.login_frame.destroy()
            self.load_main_window()
        else:
            # Failed login, show an error message
            messagebox.showerror("Login Failed", "Invalid username or password")

    def load_main_window(self):
        # load the mainframe
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack()
        tk.Label(self.main_menu, text="Welcome to our restaurant!", font="Arial 40").pack()

        # new customer button
        self.new_customer_button = tk.Button(self.main_menu, text="Add a New Customer", command=self.new_customer)
        self.new_customer_button.pack()

        # reservation button
        self.reserve_button = tk.Button(self.main_menu, text="Reserve a Table", command=self.new_reservation)
        self.reserve_button.pack()

        # show reservations button
        self.list_res_button = tk.Button(self.main_menu, text="Show Reservations", command=self.list_res_from_db)
        self.list_res_button.pack()

        # report button
        self.reports_button = tk.Button(self.main_menu, text="Reports", command=self.get_reports)
        self.reports_button.pack()

    def new_customer(self):
        self.new_customer_window = tk.Toplevel()
        self.full_name = tk.Label(self.new_customer_window, text="First name: ")
        self.full_name.grid(row=0, column=0, padx=10, pady=10)
        self.full_name_entry = tk.Entry(self.new_customer_window)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # TODO: Data validation using try and except for email format & phone no.
        # TODO: add password field and validate the data
        self.email_label = tk.Label(self.new_customer_window, text="Email address: ")
        self.email_label.grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.new_customer_window)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        self.phone_no_label = tk.Label(self.new_customer_window, text="Phone number: ")
        self.phone_no_label.grid(row=2, column=0, padx=10, pady=10)
        self.phone_no_entry = tk.Entry(self.new_customer_window)
        self.phone_no_entry.grid(row=2, column=1, padx=10, pady=10)
        self.addCus_button = tk.Button(self.new_customer_window, text="Add", command=self.add_cus_to_db)
        self.addCus_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_cus_to_db(self):
        # TODO: data validation
        self.name = self.full_name_entry.get()
        self.phone = self.phone_no_entry.get()
        self.email = self.email_entry.get()
        if not self.name or not self.phone or not self.email:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        # Insert user data into the database
        try:
            conn = sqlite3.connect("reservation_system.db")
            cursor = conn.cursor()

            # Check if a user with the same phone number already exists
            cursor.execute("SELECT * FROM Customers WHERE phone_number=?", str(self.phone))
            self.existing_user = cursor.fetchone()

            if self.existing_user:
                messagebox.showerror("Error", "User with this phone number already exists.")
                conn.close()
                return

            # Insert the new user into the User table
            cursor.execute("INSERT INTO Customers (customer_name, phone_number, email_address) VALUES (?, ?, ?)",
                           (self.name, self.phone, self.email))
            conn.commit()

            messagebox.showinfo("Success", "Registration successful.")


        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error while registering: {str(e)}")

        finally:
            conn.close()

    def new_reservation(self):
        self.new_res_window = tk.Toplevel()

        # creating a treeview to display the tables' details
        self.tables_tree = ttk.Treeview(self.new_res_window, columns=("Table Number", "Capacity"), show="headings")
        self.tables_tree.heading("Table Number", text="Table Number")
        self.tables_tree.heading("Capacity", text="Capacity")

        # adding tables to the treeview
        self.tables = get_tables()
        for table in self.tables:
            self.tables_tree.insert('', END, values=table)
        # for table in tables_list:
        #     self.tables_tree.insert("", tk.END, values=tables_list)

        # Bind the selection event of the treeview to the on_select_cleaner function
        self.tables_tree.bind("<<TreeviewSelect>>", self.on_select_table)

        # Create a label to show the selected cleaner's details
        self.selected_table_label = tk.Label(self.new_res_window, text="Selected Table: None")

        self.tables_tree.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.selected_table_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.no_of_people_label = tk.Label(self.new_res_window, text="How many people in your party?")
        self.no_of_people_label.grid(row=2, column=0, padx=10, pady=10)
        self.no_of_people_entry = tk.Entry(self.new_res_window)
        self.no_of_people_entry.grid(row=2, column=1, padx=10, pady=10)
        self.confirm_res_button = tk.Button(self.new_res_window, text="confirm", command=self.add_res_to_db)
        self.confirm_res_button.grid(row=6, column=0, columnspan=2, pady=10)

        # datetime
        self.date_entry = DateEntry(self.new_res_window, width=12, background="darkblue", foreground="white",
                                    borderwidth=2)
        self.date_entry.grid(row=4, column=0, pady=10)
        # self.table_buttons = []



    def on_select_table(self, event):
        # Get the selected table from the treeview
        self.selected_table = self.tables_tree.selection()
        if self.selected_table:
            tbl_no = self.tables_tree.item(self.selected_table, "values")[0]
            tbl_cap = self.tables_tree.item(self.selected_table, "values")[1]
            self.selected_table_label.config(text=f"Selected Cleaner: {tbl_no} for {tbl_cap} people.")

        # self.style = ttk.Style(self.new_res_window)
        # self.style.theme_use('clam')
        # self.style.configure('Treeview', foreground='#fff', background='#000' )

    #     for row in range(self.rows):
    #         table_row = []
    #         for col in range(self.columns):
    #             table_button = tk.Button(self.new_res_window, text=f"Table {col+1}", width=8, height=2)
    #             table_button.grid(row=row, column=col, padx=5, pady=5)
    #             table_row.append(table_button)
    #         self.table_buttons.append(table_row)
    #     # table_button = self.table_button[row][col]
    #     # if table_button['state'] == 'normal':
    #     #     table_button.configure(bg='lightgreen', state='disabled')
    #
    # # def selected_table(self):
    # #     sel_tab = self.table_button[]

    # def selected_tables(self, row, col):
    #     table_button = self.table_buttons[row][col]
    #     if table_button['state'] == 'normal':
    #         table_button.configure(bg='lightgreen', state='disabled')

    def confirm_reservation(self):
        selected_table = self.tables_tree.selection()
        global tbl_no
        global selected_datetime
        if selected_table:
            tbl_no = self.tables_tree.item(self.selected_table, "values")[0]
            tbl_cap = self.tables_tree.item(self.selected_table, "values")[1]
            selected_table_label.config(text=f"Selected table: {tbl_no} for {tbl_cap} people.")

            selected_datetime = self.date_entry.get()

            boolean_value = self.add_res_to_db(self, tbl_no, selected_datetime)

            if boolean_value == TRUE:
                tk.messagebox.showinfo("Successful Reservation",
                                       f'Reservation for {tbl_no}, for {tbl_cap} people on '
                                       f'{selected_datetime} is successful')

    def add_res_to_db(self, tbl_no, selected_datetime):           #IT'S NOT TAKING THE PARAMETERS AND I DON'T KNOW WHY!!
        try:
            conn = sqlite3.connect("reservation_system.db")
            cursor = conn.cursor()

            # fetching table from the db
            cursor.execute('SELECT table_num FROM TableSeating WHERE table_num=?', (tbl_no))
            customer_id = cursor.fetchone()[0]

            # cursor.execute('SELECT table_id FROM TableSeating WHERE ')
            # inserting details into the db
            cursor.execute("INSERT INTO Reservation (cust_id, table_no, reservation_date) VALUES (?, ?, ?)",
                           (customer_id, tbl_no, selected_datetime))
            conn.commit()
            return True
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f'Error while saving reservation {str(e)}')

        finally:
            conn.close()
        self.new_res_window.title("Reserve a Table")

        try:
            conn = sqlite3.connect("reservation_system.db")
            cursor = conn.cursor()

            cursor.execute("SELECT table_num, capacity FROM TableSeating WHERE phone_number=?",
                           (self.phone))
            tables_list = cursor.fetchall()

        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f'Error while fetching tables: {str(e)}')
        finally:
            conn.close()


    def list_res_from_db(self):
        self.res_history = tk.Toplevel()

        try:
            conn = sqlite3.connect("reservation_system.db.db")
            cursor = conn.cursor()

            cursor.execute("SELECT customer_id FROM Customers WHERE phone_number=?", (self.phone,))
            customer_id = cursor.fetchone()[0]

            # Fetch the booking history for the customer from the Booking table
            # cursor.execute("SELECT * FROM Booking WHERE customer_id=?", (customer_id,))
            cursor.execute(
                "SELECT r.reservation_date, c.customer_name, c.phone_number FROM Reservations r JOIN Customers c ON r.table_no = u.id WHERE c.customer_id=?",
                (customer_id,))
            reservation_history = cursor.fetchall()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error while fetching booking history: {str(e)}")
            reservation_history = []

        finally:
            conn.close()

        if not reservation_history:
            messagebox.showinfo("No Reservations", "No Reservations history available.")
            return

            # Create a listbox to display the booking history
            self.res_history.geometry('500x300')
            listbox_res_history = tk.Listbox(self.res_history, width=150)
            for i in reservation_history:
                print(i)
            # Add the booking history data to the listbox
            for res in reservation_history:
                selected_datetime, tbl_no, customer_id = reservation
                listbox_res_history.insert(tk.END,
                                               f"Date and Time: {date_time} - Cleaner Name: {cleaner_name} - Cleaner Phone: {cleaner_phone}")

            # Grid layout for the listbox
            listbox_res_history.pack(padx=10, pady=10)


    def get_reports(self):
        self.reports_window = tk.Toplevel()
        # TODO: command methods
        self.month_res_button = tk.Button(self.reports_window,
                                          text="Reservations Per Month",
                                          command=self.previous_res)  # reservation for the previous month
        self.month_res_button.pack()
        self.avg_ppl_button = tk.Button(self.reports_window, text="People Per Party",
                                        command=self.avg)  # average no. of people per party
        self.avg_ppl_button.pack()
        self.busiest_day_button = tk.Button(self.reports_window,
                                            text="Busiest Day")  # shows the day(s) with most no of reservations
        self.busiest_day_button.pack()

    def previous_res(self):
        conn = sqlite3.connect('reservation_system.db')
        df = pd.read_sql_query('SELECT * FROM Reservations')
        return df.head(30)

    def avg(self):
        conn = sqlite3.connect('reservation_system.db')
        res_li =[]
        df = pd.read_sql_query('SELECT reservation_id FROM Reservations')
        res_li.append(df)
        return res_li.mean


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantBookingApp(root)
    root.mainloop()