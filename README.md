# **Restaurant Reservation System**

## This is a Python application developed using _Tkinter_  for GUI, _SQLite_ for database management, and _Pandas_ for generating reports. The Restaurant Booking System allows users to manage customer data, table reservations, and generate various reports related to restaurant bookings.

### Features:

1. **User Authentication**:
- Users can log in using a username and password, which are stored in the database after the initial "sign up"
- The main menu is only accessible after successful login.
   
2. **Customer Management**:
- Users can add new customers to the system, including their name, email address, and phone number.
- Data validation ensures all fields are filled correctly.
   
3. **Table Reservations**:
- Users can reserve tables for a specified date and time.
- Available tables are displayed, and users can select the desired table for reservation.
- Reservation details are saved in the database.
   
4. **Reporting**:
- Three types of reports can be generated:
    - Reservations Per Month: Displays reservations made in the previous month.
    - People Per Party: Calculates the average number of people per party in reservations.
    - Busiest Day: Identifies the day(s) with the most reservations.

