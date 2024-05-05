import os
from datetime import datetime,timedelta

########################## Variables ##########################

rs_path = "C:/DDA/station/data/RS050524.D1A"   # The path to the RS file
DLG_path = "C:/DDA/station/log/DLG"  # The path to the DLG file
station_path = "C:/DDA/station/STATION.PRM" #The path to the station.prm file

########################## Functions ##########################

def open_close(rs_path, pump, nzl):
    if os.path.isfile(rs_path):
        first_line = True
        opened = False
        with open(rs_path, 'r', errors="ignore") as rs:
            for line in rs:
                if first_line:
                    first_line = False
                    continue
                if ("Open" in line):
                    if (int(line.split()[2])==nzl and int(line.split()[3])==pump):
                        opened = True
                    continue
                if ("Close" in line and opened):
                    if (int(line.split()[2])==nzl and int(line.split()[3])==pump):
                        return True
            return False
    else:
        print("RS file was not found")
        return None
                
def get_tomorrow(date):
    date_object = datetime.strptime(date, '%d%m%y')
    tomorrow = date_object + timedelta(days=1)
    return tomorrow.strftime('%d%m%y')

def get_yesterday(date):
    date_object = datetime.strptime(date, '%d%m%y')
    yesterday = date_object - timedelta(days=1)
    return yesterday.strftime('%d%m%y')

def pump_difference(rs_path, pump, nzl):
    if os.path.isfile(rs_path):
        first_line = True
        counter = 0.0
        with open(rs_path, 'r', errors="ignore") as rs:
            for line in rs:#Sum the counter starting count with all the transactions
                if first_line:
                    first_line = False
                    continue
                if "Open" in line:
                    if(int(line.split()[2]) == nzl and int(line.split()[3]) == pump and counter == 0): #This is the first open for the pump and nzl
                        counter = float(line.split()[0])
                elif (int(line.split()[3]) == nzl and int(line.split()[4]) == pump): #Finds that the pump and nzl has been opened and initializes the counter count
                    counter += float(line.split()[0])
                    continue
        with open(rs_path, 'r', errors="ignore") as rs:
            lines = rs.readlines()
            lines = lines[::-1]
            for reveresed_line in lines:#Loop from the end line to find the last closing counter of the pump and nzl and checks if it matches the total money count
                if ("Close" in reveresed_line):
                    if (int(reveresed_line.split()[2]) == nzl and int(reveresed_line.split()[3]) == pump):
                        #Money comparison with a precision of 1 digits after the decimal point
                        counter = int(counter*100)
                        counter = float(counter)/100
                        close_money_counter = float(reveresed_line.split()[0])
                        close_money_counter = int(close_money_counter*100)
                        close_money_counter = float(close_money_counter)/100
                        str = str(counter - close_money_counter)
                        index = str.index('.')
                        if len(str) - index > 3:
                            str = str[:index+2]
                        if abs(counter - close_money_counter) > 1:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference of " + str + " in the counter")
                            return True, (counter - close_money_counter)
                        else:
                            return False, 0.0
            return False, 999999
    else:
        print("RS file was not found")
        return None

def next_rs(rs_path):
    last_char = rs_path[-1]
    next_char = chr(ord(last_char) + 1) if last_char.isalpha() and ord(last_char) < ord('Z') else last_char
    modified_rs_path = rs_path[:-1] + next_char
    if os.path.isfile(modified_rs_path):
        return modified_rs_path
    else:
        date = rs_path[-10:-4]
        next_rs = rs_path[:-10] + get_tomorrow(date) + rs_path[-4:-1] + "A"
        return next_rs

def get_closing_time(rs_path):
    if os.path.isfile(rs_path):
        with open(rs_path, 'r', errors="ignore") as rs:
            lines = rs.readlines()
            lines = lines[::-1]
            for reveresed_line in lines:#Loop from the end line to find the last closing counter of the pump and nzl and checks if it matches the total money count
                if ("Close" in reveresed_line):
                    return reveresed_line.split[5], reveresed_line.split[6]
    else:
        print("RS file was not found")
        return None

def close_pump(rs_path, pump, nzl, counter):
    new_rs_path = next_rs(rs_path)
    if os.path.isfile(new_rs_path):
        first_line = True
        with open(new_rs_path, 'r', errors="ignore") as rs:
            for line in rs:
                if first_line:
                    first_line = False
                    continue
                if ("Open" in line):
                    if (int(line.split()[2])==nzl and int(line.split()[3])==pump and (abs(float(line.split()[0])-counter)<1)):
                        with open('rs_path', 'a') as rs:
                            line_to_write = line.replace("Open ", "Close")
                            line_to_write = line_to_write.replace("000000", "999999")
                            line_to_write = line_to_write.replace(line.split()[5], get_closing_time(rs_path)[0])
                            rs.write(line)
                            line_to_write = line_to_write.replace(line.split()[6], get_closing_time(rs_path)[1])
                            rs.write(line_to_write)
                            return True
                if ("Close" in line):
                    if (int(line.split()[2])==nzl and int(line.split()[3])==pump and (abs(float(line.split()[0])-counter)<1)):
                        with open('rs_path', 'a') as rs:
                            line_to_write = line.replace(line.split()[5], get_closing_time(rs_path)[0])
                            line_to_write = line_to_write.replace(line.split()[6], get_closing_time(rs_path)[1])
                            rs.write(line_to_write)
                            return True
            print("Couldn't find a closing line for pump: " + str(pump) + " and nozzle: " + str(nzl))
            print("You'll have to close the pump manually...")
            print("There's a probability that the pump was closed and has another difference in the counter")
            return False
    else:
        print("Couldn't find the next RS and so closing the pump was not successful")
        return None
    
def positive_difference(rs_path, pump, nzl):
    print("There's a positive difference in the counter of the pump: " + str(pump) + " and nozzle: " + str(nzl) + " and I haven't written the code to fix that :)")
    return None

def negative_difference(rs_path, pump, nzl):
    print("There's a negative difference in the counter of the pump: " + str(pump) + " and nozzle: " + str(nzl) + " and I haven't written the code to fix that :)")
    return None

########################## Main ##########################

if os.path.isfile(station_path):
    with open(station_path, 'r', errors="ignore") as station_file:
        first_line = True
        for line in station_file:
            if first_line:
                first_line = False
                continue
            if (line.split()[0].isdigit() and line.split()[4].isdigit()):
                pump = int(line.split()[0])
                nzl = int(line.split()[4])
                is_difference, difference = pump_difference(rs_path, pump, nzl)
                if(is_difference):
                    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference in the counter of " + str(difference)) 
                    if(difference>300):
                        close_pump(rs_path, pump, nzl, difference)
                    elif(difference>0):
                        positive_difference(rs_path, pump, nzl)
                    elif(difference<0):
                        negative_difference(rs_path, pump, nzl)
else:
    print("Couldn't find the station file in the path: " + station_path)
input()