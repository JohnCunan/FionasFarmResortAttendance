from datetime import datetime


# Convert 12-Hour format to 24-Hour format
def convert(time):
    if time[-2:] == 'AM':
        if time[:2] == '12':
            converted = str('00' + time[2:8])
        else:
            converted = time[:-2]
    else:
        if time[:2] == '12':
            converted = time[:-2]
        else:
            converted = str(int(time[:2]) + 12) + time[2:8]

    return converted


# Compute total hours
def get_total_hours(time_in, time_out):
    time_1 = datetime.strptime(time_in, "%I:%M:%S %p")
    time_2 = datetime.strptime(time_out, "%I:%M:%S %p")

    time_interval = time_2 - time_1
    return time_interval


def get_total_ot_hours(end_time, time_out):
    time_1 = datetime.strptime(end_time, "%H:%M:%S")
    time_2 = datetime.strptime(time_out, "%H:%M:%S")

    time_interval = time_2 - time_1
    return time_interval
