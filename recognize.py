import os
import sys
import PIL
import cv2
import pickle
import numpy as np
from tkinter import *
import tkinter.font as font
from train import train_model
from PIL import Image, ImageTk
from collect import collect_photos
from clock import get_time, get_date
from time_diff import convert, get_total_ot_hours
from play_audio import play_time_in_audio, play_time_out_audio
from pop_ups import model_error_message, camera_error_message, restart_message, training_message, db_saved_message, \
    employee_detected_error_message

# Haar Cascade Variables
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# GUI Variables
root = Tk()
root.bind('<Escape>', lambda e: sys.exit())
root.geometry('1000x900')
root.title('Face Recognition Attendance System')  # Window Title
root.resizable(False, False)  # Make Window not resizable
root['background'] = '#396544'

lmain = Label(root)
lmain.grid(padx=20, pady=20)

# Load saved db name
with open('Persistence Files/db_name.pickle', 'rb') as f:
    database_name = pickle.load(f)


def add_db_name():
    locate_db_button.place_forget()
    db_textbox.config(state=NORMAL)
    cancel_db_button.config(state=NORMAL)
    save_db_button.place(x=370, y=830)


def cancel_db_add():
    save_db_button.place_forget()
    db_textbox.delete(0, END)
    db_textbox.insert(0, database_name)
    db_textbox.config(state=DISABLED)
    cancel_db_button.config(state=DISABLED)
    locate_db_button.place(x=370, y=830)


# Locate DB button and text box
db_textbox = Entry(root, width=58)
db_textbox.insert(0, database_name)  # Server=DESKTOP-N4JRA7K\SQLEXPRESS;
db_textbox.place(x=520, y=833)
db_textbox.config(state=DISABLED)


# Get DB server
def save_db_name():
    db_name = db_textbox.get()
    # Create persistence file
    with open('Persistence Files/db_name.pickle', 'wb') as f:
        pickle.dump(db_name, f)

    save_db_button.place_forget()
    cancel_db_button.config(state=DISABLED)
    locate_db_button.place(x=370, y=830)
    db_textbox.config(state=DISABLED)
    db_saved_message()
    sys.exit()


# Locate db button
locate_db_button = Button(root, text='Locate Database Server ', command=add_db_name)
locate_db_button.place(x=370, y=830)

# Save db button
save_db_button = Button(root, text='                 Save                 ', command=save_db_name)

# Cancel button for save db
cancel_db_button = Button(root, text='   Cancel   ', command=cancel_db_add)
cancel_db_button.place(x=880, y=830)
cancel_db_button.config(state=DISABLED)


# Add employee button and text box
def add_new_employee_name():
    add_emp_textbox.config(state=NORMAL)
    cancel_add_button.config(state=NORMAL)
    add_emp_textbox.insert(0, 'Enter employee name')
    add_employee_button.place_forget()
    capture_face_button.place(x=370, y=800)


def cancel_add_employee():
    add_emp_textbox.delete(0, END)
    add_emp_textbox.config(state=DISABLED)
    cancel_add_button.config(state=DISABLED)
    capture_face_button.place_forget()
    add_employee_button.place(x=370, y=800)


add_emp_textbox = Entry(root, width=58)
add_emp_textbox.insert(0, ' ')
add_emp_textbox.place(x=520, y=803)
add_emp_textbox.config(state=DISABLED)

# Cancel button for add new employee
cancel_add_button = Button(root, text='   Cancel   ', command=cancel_add_employee)
cancel_add_button.place(x=880, y=800)
cancel_add_button.config(state=DISABLED)


# Add new employee and capture employee face
def capture_employee_face():
    collect_photos(add_emp_textbox.get(), cap, face_cascade)


add_employee_button = Button(root, text='        Add Employee        ', command=add_new_employee_name)
add_employee_button.place(x=370, y=800)

# Capture faces button
capture_face_button = Button(root, text='         Capture face          ', command=capture_employee_face)

# Locate Trainer Model File Directory (YML)
try:
    recognizer.read('trainer.yml')  # WILL ERROR AT FIRST STARTUP BECAUSE THERE IS NO TRAINED MODEL YET
except cv2.error as e:
    model_error_message()

labels = {"person_name": 1}  # WILL ERROR AT FIRST STARTUP BECAUSE THERE IS NO TRAINED MODEL YET

# Load saved employee name labels (PICKLE)
with open('Persistence Files/labels.pickle', 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

# Camera Variable
cap = cv2.VideoCapture(0)

# Variable to use when inserting attendance record
detected_face = None


# Loop makes capturing continuous
def show_frame():
    ret, frame = cap.read()

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # No Camera Error
    except cv2.error as e:
        camera_error_message()
        sys.exit()

    # Black rectangle
    cv2.rectangle(frame, (0, 900), (2100, 440), (0, 0, 0), thickness=cv2.FILLED)

    # Write Text
    cv2.putText(frame, 'Date: ' + get_date(), (7, 465), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Time: ' + get_time(), (250, 465), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)

    # Resize the frames
    width = int(frame.shape[1] * 1.5)
    height = int(frame.shape[0] * 1.5)
    dimensions = (width, height)
    resize_frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
    resize_gray = cv2.resize(gray, dimensions, interpolation=cv2.INTER_AREA)

    # Detect Face
    faces = face_cascade.detectMultiScale(resize_gray, scaleFactor=1.3, minNeighbors=3)  # 1.5 & 2

    # For every detected face identify the person
    for (x, y, w, h) in faces:
        # Get the Region of Interest (The face)
        roi_gray = resize_gray[y:y + h, x:x + w]
        roi_color = resize_frame[y:y + h, x:x + w]

        # Draw Rectangle on the detected Region of Interest
        color = (255, 0, 0)
        stroke = 4
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(resize_frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        # Recognize Face
        id_, conf = recognizer.predict(roi_gray)
        # 40 <= conf <= 90
        if 30 <= conf <= 90:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(resize_frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

            # Declare detected_face as a global variable
            global detected_face
            detected_face = labels[id_]

        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = 'Unknown'
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(resize_frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            detected_face = None

    # Show camera in the window
    cv2image = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


# Check if the database is connected (get_attendance.py)
db_connected = False
try:
    from get_attendance import time_in, time_out, total_hours, late_or_not, ot_hours, conn
    from get_attendance import get_employee_time_out, get_employee_time_in, get_total_hours
    from get_attendance import get_employee_start_time, get_employee_end_time, check_allowed_ot

    db_connected = True
except ImportError:
    pass


# Record attendance functions
# Employee time in
def btn_time_in():
    employee = detected_face

    if employee is not None:
        play_time_in_audio()
        time_in(conn, detected_employee=employee)

        # Check employee start schedule
        start_time = convert(get_employee_start_time(employee))
        in_time = convert(get_time())
        late = None

        # Check if employee is late
        if in_time > start_time:
            late = True  # Employee is late
        else:
            late = False  # Employee is not late

        # Record into DB if late or not
        late_or_not(conn, detected_employee=employee, status=late)
    else:
        employee_detected_error_message()
        return


# Employee time out
def btn_time_out():
    employee = detected_face

    if employee is not None:
        play_time_out_audio()
        time_out(conn, detected_employee=employee)

        # Calculate Total Hours
        employee_time_in = get_employee_time_in(employee, get_date())
        employee_time_out = get_employee_time_out(employee, get_date())
        t_hours = get_total_hours(employee_time_in, employee_time_out)

        # if Time in at PM then Time out at AM remove the '-1 day' from the total hours
        if str(t_hours).find('-') != -1:
            t_hours = str(t_hours)[8:]

        # Calculate overtime
        ot_total = '00:00:00'
        allowed_ot = check_allowed_ot(employee)

        if allowed_ot == 'True':
            end_time = convert(get_employee_end_time(employee)).rstrip()
            out_time = convert(get_time()).rstrip()

            if out_time > end_time:
                ot_total = get_total_ot_hours(end_time, out_time)

                if str(ot_total) > '3:00:00':
                    ot_total = '03:00:00'

        ot_hours(conn, detected_employee=employee, total_ot_hours=ot_total)

        # Insert employee total hours into DB
        total_hours(conn, detected_employee=employee, total_work_hours=str(t_hours))
    else:
        employee_detected_error_message()
        return


# Db not found text
db_not_found_label = Label(root, text='Database Not Connected, Time in and Out Buttons are disabled', bg='#396544',
                           fg='white', font='none 10 bold')

# Button variables
button_font = font.Font(family='Tahoma', size=20, underline=0)

time_in_button = Button(root, text='Time In', height=2, width=10, font=button_font, command=btn_time_in)
time_in_button.place(x=23, y=770)

time_out_button = Button(root, text='Time Out', height=2, width=10, font=button_font, command=btn_time_out)
time_out_button.place(x=190, y=770)

if not db_connected:
    time_in_button.config(state=DISABLED)
    time_out_button.config(state=DISABLED)
    db_not_found_label.place(x=23, y=860)

# Train text
train_text_label = Label(root, text=' ', bg='#396544', fg='white', font='none 14 bold')
train_text_label.place(x=520, y=770)


def train():
    time_in_button.config(state=DISABLED)
    time_out_button.config(state=DISABLED)
    train_text_label.config(text='Training model, please wait...')
    training_message()
    train_model()
    train_text_label.config(text='Training Complete')
    restart_message()
    sys.exit()


# Train button
train_model_button = Button(root, text='          Train Model           ', command=train)
train_model_button.place(x=370, y=770)

show_frame()
root.mainloop()
