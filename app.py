import streamlit as st
import pandas as pd
import subprocess

st.title("Clockwise: Attendance Management System")
def run_helper(name,roll):
    st.write("Running add_faces...")

    if name and roll:

        process = subprocess.Popen(
            ["python", "add_faces.py", name, roll],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = process.communicate()

        if output:
            st.write(output.decode("utf-8"))  # Display output if there is any

        if error:
            st.error(
                "Error occurred while running add_faces: " + error.decode("utf-8")
            )  # Display error if there is any
        else:
            st.success("add_faces executed successfully.")

st.subheader("Train the Face Recognition Model")
with st.form("input_form"):

    name = st.text_input("Enter name:")
    roll = st.text_input("Enter roll number:")

    
    submitted = st.form_submit_button("Submit")

    
    if submitted:
        run_helper(name, roll)


def run_test():
    st.write("Running test.py...")
    process = subprocess.Popen(["python", "test.py"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        st.write(output.decode("utf-8"))  # Display output if there is any
    if error:
        st.error("Error occurred while running test.py")
    else:
        st.success("test.py executed successfully.")


# Button to run test.py
if st.button("Run Face Recognition Model"):
    run_test()
