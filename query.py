import mysql.connector
from datetime import datetime, timedelta

# Establish connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13Lock02",
    database="Attendance",
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()


# Function to insert a new record into the attendance_records table
def insert_record():
    name = input("Enter student name: ")
    roll_no = int(input("Enter roll number: "))
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM:SS): ")
    sql = "INSERT INTO attendance_records (name, roll_no, date, time) VALUES (%s, %s, %s, %s)"
    values = (name, roll_no, date, time)
    cursor.execute(sql, values)
    db_connection.commit()
    print("Record inserted successfully.")


# Helper function to print records with proper formatting
def print_records(records):
    for record in records:
        name = record[0]
        roll_no = record[1]
        date = record[2].strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
        time = str(record[3])  # Format time as HH:MM:SS
        formatted_record = (
            f"Name: {name}, Roll No: {roll_no}, Date: {date}, Time: {time}"
        )
        print(formatted_record)


# Function to retrieve all records from the attendance_records table
def get_all_records():
    cursor.execute("SELECT * FROM attendance_records")
    records = cursor.fetchall()
    
    print_records(records)


# Function to retrieve records by student name
def get_records_by_name():
    name = input("Enter student name: ")
    cursor.execute("SELECT * FROM attendance_records WHERE name = %s", (name,))
    records = cursor.fetchall()
    print_records(records)


# Function to update attendance time for a student on a specific date
def update_attendance_time():
    name = input("Enter student name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    new_time = input("Enter new time (HH:MM:SS): ")
    sql = "UPDATE attendance_records SET time = %s WHERE name = %s AND date = %s"
    values = (new_time, name, date)
    cursor.execute(sql, values)
    db_connection.commit()
    print("Attendance time updated successfully.")


# Function to delete records by student name
def delete_records_by_name():
    name = input("Enter student name: ")
    sql = "DELETE FROM attendance_records WHERE name = %s"
    cursor.execute(sql, (name,))
    db_connection.commit()
    print("Records deleted successfully.")


# Function to count total records in the table
def count_records():
    cursor.execute("SELECT COUNT(*) FROM attendance_records")
    count = cursor.fetchone()[0]
    print("Total records:", count)


# Function to display distinct roll numbers
def display_distinct_roll_numbers():
    cursor.execute("SELECT DISTINCT roll_no FROM attendance_records")
    roll_numbers = cursor.fetchall()
    for roll in roll_numbers:
        print(roll[0])


# Function to display records ordered by date and time
def display_records_ordered():
    cursor.execute("SELECT * FROM attendance_records ORDER BY date, time")
    records = cursor.fetchall()
    print_records(records)


# Function to summarize attendance for each student
def summarize_attendance():
    cursor.execute("SELECT name, COUNT(*) FROM attendance_records GROUP BY name")
    summaries = cursor.fetchall()
    for summary in summaries:
        print(f"{summary[0]}: {summary[1]}")


# Menu options
def display_menu():
    print("\nAttendance Management System Menu:")
    print("1. Insert a new record")
    print("2. Retrieve all records")
    print("3. Retrieve records by student name")
    print("4. Update attendance time")
    print("5. Delete records by student name")
    print("6. Count total records")
    print("7. Display distinct roll numbers")
    print("8. Display records ordered by date and time")
    print("9. Summarize attendance")
    print("0. Exit")


# Main function to run the menu-based system
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ")

        if choice == "1":
            insert_record()
        elif choice == "2":
            get_all_records()
        elif choice == "3":
            get_records_by_name()
        elif choice == "4":
            update_attendance_time()
        elif choice == "5":
            delete_records_by_name()
        elif choice == "6":
            count_records()
        elif choice == "7":
            display_distinct_roll_numbers()
        elif choice == "8":
            display_records_ordered()
        elif choice == "9":
            summarize_attendance()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option (0-9).")

    # Close the database connection
    cursor.close()
    db_connection.close()


# Execute the main function
if __name__ == "__main__":
    main()
