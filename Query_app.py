import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import os


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13Lock02",
    database="Attendance",
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()


# Streamlit app layout
def main():
    st.title("Clockwise: Attendance Management System")
    st.subheader("Welcome to Clockwise Attendance Management System!")
    menu_options = [
        "Home",
        "Open CSV file",
        "Insert a New Record",
        "Retrieve All Records",
        "Retrieve Records by Student Name",
        "Retrieve Records by Date",
        "Delete Records by Student Name",
        "Count Total Records",
        "Display Distinct Roll Numbers",
        "Display Records Ordered by Date and Time",
        "Summarize Attendance",
    ]

    choice = st.selectbox("Menu", menu_options)
    if choice == "Home":
        st.subheader("")
    elif choice == "Open CSV file":
        open_csv()
    elif choice == "Insert a New Record":
        insert_record()
    elif choice == "Retrieve All Records":
        get_all_records()
    elif choice == "Retrieve Records by Student Name":
        get_records_by_name()
    elif choice == "Retrieve Records by Date":
        get_records_by_date()
    elif choice == "Delete Records by Student Name":
        delete_records_by_name()
    elif choice == "Count Total Records":
        count_records()
    elif choice == "Display Distinct Roll Numbers":
        display_distinct_roll_numbers()
    elif choice == "Display Records Ordered by Date and Time":
        display_records_ordered()
    elif choice == "Summarize Attendance":
        summarize_attendance()

def  open_csv():
    st.title("CSV File Viewer")

    # Collect user input for date using date picker
    file_date = st.date_input("Select a date:")
    st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")
    # Check if a date is selected
    if file_date:
        try:
            # Format the selected date as YYYY-MM-DD
            formatted_date = file_date.strftime("%Y-%m-%d")
            file_path = f"Attendance/Attendance_{formatted_date}.csv"

            # Check if the file exists
            if os.path.exists(file_path):
                # Load CSV file using pandas
                df = pd.read_csv(file_path)

                # Display the DataFrame
                st.write("### CSV File Contents:")
                st.write(df)
            else:
                st.error("File not found. Please select another date.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please select a date to view the corresponding CSV file.")


# Function to insert a new record into the attendance_records table
def insert_record():
    name = st.text_input("Enter student name:")
    roll_no = st.number_input("Enter roll number:")
    date = st.date_input("Enter date:")
    time = st.time_input("Enter time:")

    if st.button("Insert Record"):
        sql = "INSERT INTO attendance_records (name, roll_no, date, time) VALUES (%s, %s, %s, %s)"
        values = (name, roll_no, date, time)
        cursor.execute(sql, values)
        db_connection.commit()
        st.success("Record inserted successfully.")


# Function to retrieve all records from the attendance_records table
def get_all_records():
    cursor.execute("SELECT * FROM attendance_records")
    records = cursor.fetchall()

    if not records:
        st.write("No records found.")
    else:
        st.write("### Attendance Records:")
        for record in records:
            formatted_record = f"Name: {record[0]},   Roll No: {record[1]},    Date: {record[2]},   Time: {record[3]}"
            st.write(formatted_record)


# Function to retrieve records by student name
def get_records_by_name():
    name = st.text_input("Enter student name:")
    if st.button("Retrieve Records"):
        cursor.execute("SELECT * FROM attendance_records WHERE name = %s", (name,))
        records = cursor.fetchall()

        if not records:
            st.write("No records found.")
        else:
            st.write("### Attendance Records:")
            for record in records:
                formatted_record = f"Name: {record[0]}, Roll No: {record[1]}, Date: {record[2]}, Time: {record[3]}"
                st.write(formatted_record)


# Function to get attendance data for a student in a date interval
def get_records_by_date():
    name = st.text_input("Enter student name:")
    datef = st.date_input("Date from:")
    datet = st.date_input("Date to:")
    if st.button("Retrieve Records"):
    
        # Convert date inputs to datetime objects
        datef = datetime.combine(datef, datetime.min.time())
        datet = datetime.combine(datet, datetime.max.time())

        if name and datef <= datet:
            try:

                # Query attendance records within the date range
                query = "SELECT * FROM attendance_records WHERE name = %s AND date BETWEEN %s AND %s"
                cursor.execute(query, (name, datef, datet))
                records = cursor.fetchall()

                # Display the retrieved records
                st.write(f"Attendance records for {name} between {datef.date()} and {datet.date()}:")
                if records:
                    for record in records:
                        date = record[2]  # Format date as YYYY-MM-DD
                        time = record[3]  # Format time as HH:MM:SS
                        st.write(f"Date: {date}, Time: {time}")
                else:
                    st.write("No records found for the specified date range.")
            except Exception as e:
                st.error(f"Error occurred: {e}")
        else:
            st.warning("Please enter valid inputs for student name and date range.")


# Function to delete records by student name
def delete_records_by_name():
    name = st.text_input("Enter student name:")
    if st.button("Delete Records"):
        sql = "DELETE FROM attendance_records WHERE name = %s"
        cursor.execute(sql, (name,))
        db_connection.commit()
        st.success("Records deleted successfully.")


# Function to count total records in the table
def count_records():
    cursor.execute("SELECT COUNT(*) FROM attendance_records")
    count = cursor.fetchone()[0]
    st.write(f"Total records: {count}")


# Function to display distinct roll numbers
def display_distinct_roll_numbers():
    cursor.execute("SELECT DISTINCT roll_no FROM attendance_records")
    roll_numbers = cursor.fetchall()
    st.write("### Distinct Roll Numbers:")
    for roll in roll_numbers:
        st.write(roll[0])


# Function to display records ordered by date and time
def display_records_ordered():
    cursor.execute("SELECT * FROM attendance_records ORDER BY date, time")
    records = cursor.fetchall()

    if not records:
        st.write("No records found.")
    else:
        st.write("### Attendance Records Ordered by Date and Time:")
        for record in records:
            formatted_record = f"Name: {record[0]}, Roll No: {record[1]}, Date: {record[2]}, Time: {record[3]}"
            st.write(formatted_record)


# Function to summarize attendance for each student
def summarize_attendance():
    cursor.execute("SELECT name, COUNT(*) FROM attendance_records GROUP BY name")
    summaries = cursor.fetchall()

    if not summaries:
        st.write("No attendance data found.")
    else:
        st.write("### Attendance Summary:")
        for summary in summaries:
            st.write(f"{summary[0]}: {summary[1]}")


# Run the Streamlit app
if __name__ == "__main__":
    main()
