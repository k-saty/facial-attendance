from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import mysql.connector
from datetime import datetime
import time
import csv

COL_NAMES = ["NAME", "DATE", "TIME"]
try:
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="13Lock02", database="Attendance"
    )
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")
    exit()

mycursor = mydb.cursor()

try:
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS attendance_records (name VARCHAR(255), roll_no INT PRIMARY KEY, date DATE, time TIME)"
    )
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS student_info (roll_no INT  PRIMARY KEY,name VARCHAR(255) NOT NULL )"
    )
except mysql.connector.Error as e:
    print(f"Error creating tables: {e}")

try:
    with open("data/names.pkl", "rb") as w:
        LABELS = pickle.load(w)
    with open("data/faces_data.pkl", "rb") as f:
        FACES = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error loading face data: {e}")
    exit()

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")

video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error opening video capture device")
    exit()

while True:
    ret, frame = video.read()
    if not ret:
        print("Error reading frame from video capture device")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(
        "data/haarcascade_frontalface_default.xml"
    ).detectMultiScale(gray, 1.3, 5)
    attendance = None

    for x, y, w, h in faces:
        crop_img = frame[y : y + h, x : x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        cv2.rectangle(frame, (x, y - 40), (x + w, y), (0, 0, 255), -1)
        cv2.putText(
            frame,
            str(output[0]),
            (x, y - 15),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 255, 255),
            1,
        )

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        attendance = [str(output[0]), date, timestamp]

    imgBackground[162:642, 55:695] = frame[120:600, 320:960]

    screen_width = 1920
    screen_height = 1080
    resized_frame = cv2.resize(imgBackground, (screen_width, screen_height))
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Frame", resized_frame)

    k = cv2.waitKey(1)
    if k == ord("o"):
        if attendance:
            os.system("afplay data/Glass.aiff")
            if exist:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)
            else:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
            csvfile.close()
            try:
                sql = "INSERT INTO attendance_records (name, roll_no, date, time) VALUES (%s, %s, %s, %s)"
                roll_sql = "SELECT roll_no FROM student_info WHERE name = %s"
                roll_val = (attendance[0],)
                mycursor.execute(roll_sql, roll_val)
                roll_result = mycursor.fetchone()
                roll_no = roll_result[0]
                val = (attendance[0], roll_no, attendance[1], attendance[2])
                mycursor.execute(sql, val)
                mydb.commit()
                print(f"Attendance for {attendance[0]} has been recorded.")
                cv2.putText(
                    resized_frame,
                    f"Attendance for {attendance[0]} has been recorded",
                    (150, 950),
                    cv2.FONT_HERSHEY_COMPLEX,
                    2,
                    (0, 255, 0),
                    5,
                )
                cv2.imshow("Frame", resized_frame)
                cv2.waitKey(2000)
            except mysql.connector.Error as e:
                print(f"Error recording attendance: {e}")

    if k == ord("q"):
        break

mydb.close()
video.release()
cv2.destroyAllWindows()
