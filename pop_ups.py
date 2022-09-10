from tkinter import messagebox


def model_error_message():
    messagebox.showwarning('Trainer model', 'Trainer model is missing, please locate the file')


def camera_error_message():
    messagebox.showerror('Error', 'Camera is not detected, exiting program...')


# def database_error_message():
#     messagebox.showwarning('Warning', 'Database is not detected, Please Connect the database')


# def labels_error_message():
#     messagebox.showerror('Labels', 'Labels not found, please locate the file named labels.pickle')


def restart_message():
    messagebox.showinfo('Info', 'Training Complete, re-open the application in order for changes to '
                                'takes effect')


def timeout_error_message():
    messagebox.showwarning('Warning', 'Employee can not time out before timing in')


def employee_detected_error_message():
    messagebox.showerror('Error', 'No recognized employee detected')


def employee_already_exist_message():
    messagebox.showwarning('Warning', 'Employee Already Exists')


def collect_finished_message():
    messagebox.showinfo('Info', 'Collection Finished')


def training_message():
    messagebox.showinfo('Info', 'Model for face recognition will be trained, you will not be able to use '
                                'the attendance system while the model is being trained \n'
                                '\nClick "Ok" to start training')


def db_saved_message():
    messagebox.showinfo('Info', 'Database server location saved, re-open the application for the changes to take effect')
