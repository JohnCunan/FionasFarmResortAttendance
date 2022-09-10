import re
import pickle
import pyodbc
from datetime import datetime
from clock import get_time, get_date
from pop_ups import timeout_error_message


with open('Persistence Files/db_name.pickle', 'rb') as f:
    database_name = pickle.load(f)

try:
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=" + database_name + ';' +
        "Database=AttendanceModuleTest;"  # pyodbc.InterfaceError
        "Trusted_Connection=yes;"
    )
except pyodbc.OperationalError as err:
    pass


def time_in(conn, detected_employee):
    cursor = conn.cursor()
    cursor.execute(
        "IF NOT EXISTS (SELECT EmployeeName, Date FROM AttendanceSheet WHERE EmployeeName='" + detected_employee + "'" + " AND Date='" + get_date() + "')"
        "BEGIN "
        "INSERT INTO AttendanceSheet(EmployeeName, TimeIn, Date) values(?, ?, ?)"
        "END",
        (detected_employee, get_time(), get_date())
    )
    conn.commit()


def time_out(conn, detected_employee):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE AttendanceSheet SET TimeOut='" + get_time() + "' "
        "WHERE EmployeeName='" + detected_employee + "' AND Date='" + get_date() + "' AND TimeOut IS NULL"
    )
    conn.commit()


def total_hours(conn, detected_employee, total_work_hours):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE AttendanceSheet SET TotalHours='" + str(total_work_hours) + "' "
        "WHERE EmployeeName='" + detected_employee + "' AND Date='" + get_date() + "' AND TotalHours IS NULL"
    )
    conn.commit()


def late_or_not(conn, detected_employee, status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE AttendanceSheet SET Late='" + str(status) + "' "
        "WHERE EmployeeName='" + detected_employee + "' AND Date='" + get_date() + "' AND Late IS NULL"
    )
    conn.commit()


def ot_hours(conn, detected_employee, total_ot_hours):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE AttendanceSheet SET OvertimeHours='" + str(total_ot_hours) + "' "
        "WHERE EmployeeName='" + detected_employee + "' AND Date='" + get_date() + "' AND OvertimeHours IS NULL"
    )
    conn.commit()


# Return employee schedule (Get total hours)
def get_employee_time_in(name, date):
    cursor = conn.cursor()
    cursor.execute("SELECT TimeIn FROM AttendanceSheet "
                   "WHERE Date='" + date + "' AND EmployeeName='" + name + "'")
    for row in cursor:
        time = str(row)
        return re.sub("[(',)]", '', time).rstrip()


def get_employee_time_out(name, date):
    cursor = conn.cursor()
    cursor.execute("SELECT TimeOut FROM AttendanceSheet "
                   "WHERE Date='" + date + "' AND EmployeeName='" + name + "'")
    for row in cursor:
        time = str(row)
        return re.sub("[(',)]", '', time).rstrip()


def get_total_hours(time_in, time_out):
    try:
        time_1 = datetime.strptime(time_in, "%I:%M:%S %p")
        time_2 = datetime.strptime(time_out, "%I:%M:%S %p")

        time_interval = time_2 - time_1
        return time_interval
    except TypeError:
        timeout_error_message()


# Check employee schedules (Late or not Late)

def get_employee_start_time(name):
    cursor = conn.cursor()
    cursor.execute("SELECT StartTime FROM EmployeeSchedule "
                   "WHERE EmployeeName='" + name + "'")
    for row in cursor:
        time = str(row)
        return re.sub("[(',)]", '', time).rstrip()


def get_employee_end_time(name):
    cursor = conn.cursor()
    cursor.execute("SELECT EndTime FROM EmployeeSchedule "
                   "WHERE EmployeeName='" + name + "'")
    for row in cursor:
        time = str(row)
        return re.sub("[(',)]", '', time).rstrip()


def check_allowed_ot(name):
    cursor = conn.cursor()
    cursor.execute("SELECT AllowedOT FROM EmployeeSchedule "
                   "WHERE EmployeeName='" + name + "'")
    for row in cursor:
        time = str(row)
        return re.sub("[(',)]", '', time).rstrip()