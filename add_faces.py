import cv2
import pickle
import numpy as np
import os
import mysql.connector
from datetime import datetime
import argparse


def run_addfaces(name, roll):

    mydb = mysql.connector.connect(host="localhost", user="root", password="13Lock02")

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS Attendance")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="13Lock02",
        database="Attendance",
    )
    mycursor = mydb.cursor()

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS student_info (roll_no INT  PRIMARY KEY,name VARCHAR(255) NOT NULL )"
    )

    screen_width = 1920
    screen_height = 1080

    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
    faces_data = []

    i = 0

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        biggest_face = None
        max_area = 0

        for x, y, w, h in faces:
            area = w * h
            if area > max_area:
                max_area = area
                biggest_face = (x, y, w, h)

        if biggest_face is not None:
            x, y, w, h = biggest_face
            crop_img = frame[y : y + h, x : x + w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            if len(faces_data) <= 100 and i % 5 == 0:
                faces_data.append(resized_img)
            i += 1
            cv2.putText(
                frame,
                str(len(faces_data)) + "/100",
                (50, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (50, 50, 255),
                3,
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Frame", frame)

        k = cv2.waitKey(1)
        if k == ord("q") or len(faces_data) == 100:
            break

    video.release()
    cv2.destroyAllWindows()

    if k != ord("q"):
        check_sql = "SELECT * FROM student_info WHERE roll_no = %s"
        check_val = (roll,)
        mycursor.execute(check_sql, check_val)
        existing_student = mycursor.fetchone()

        if existing_student:
            print(f"Student with roll number {roll} already exists.")
        else:
            try:
                sql = "INSERT INTO student_info (name, roll_no) VALUES (%s, %s)"
                val = (name, roll)
                mycursor.execute(sql, val)
                mydb.commit()
                print(f"Student {name} with roll number {roll} has been added.")
            except mysql.connector.Error as e:
                print(f"Error adding student: {e}")

        mydb.close()

        faces_data = np.asarray(faces_data)
        faces_data = faces_data.reshape(100, -1)

        try:
            with open("data/names.pkl", "rb") as f:
                names = pickle.load(f)
            names = names + [name] * 100
            with open("data/names.pkl", "wb") as f:
                pickle.dump(names, f)
        except FileNotFoundError:
            names = [name] * 100
            with open("data/names.pkl", "wb") as f:
                pickle.dump(names, f)

        try:
            with open("data/faces_data.pkl", "rb") as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open("data/faces_data.pkl", "wb") as f:
                pickle.dump(faces, f)
        except FileNotFoundError:
            with open("data/faces_data.pkl", "wb") as f:
                pickle.dump(faces_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="Name of the student")
    parser.add_argument("roll", type=str, help="Roll number of the student")
    args = parser.parse_args()
    run_addfaces(args.name, args.roll)
