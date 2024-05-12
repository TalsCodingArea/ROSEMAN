import os
import sys
from datetime import datetime


def open_close(rs_path, pump, nzl):
    first_line = True
    opened = False
    if not os.path.isfile(rs_path):
        #print("File not found")
        return False
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            for line in rs_file:
                if first_line:
                    first_line = False
                    continue
                if "Open" in line:
                    if (int(line.split()[2]) == nzl and int(line.split()[3]) == pump):
                        opened = True
                    continue
                if ("Close" in line and opened):
                    if (int(line.split()[2]) == nzl and int(line.split()[3]) == pump):
                        return True
            return False

def pump_difference(rs_path, pump, nzl):
    first_line = True
    money = 0.0
    if not os.path.isfile(rs_path):
        print("RS file not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            for line in rs_file:#Sum the money starting count with all the transactions
                if first_line:
                    first_line = False
                    continue
                if "Open" in line:
                    if(int(line.split()[2]) == nzl and int(line.split()[3]) == pump and money == 0): #This is the first open for the pump and nzl
                        money = float(line.split()[0])
                    elif(int(line.split()[2]) == nzl and int(line.split()[3]) == pump and money != 0): #This is not the first opening for the pump and nzl so we compare the money counter
                        if(abs(money - float(line.split()[0])) > 1):
                            dif = int(abs(money - float(line.split()[0]))*100)
                            dif = float(dif)/100
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference in the counter of " + str(dif) + " before the opening at " + line.split()[5])
                            return False
                elif ("Close" not in line and int(line.split()[3]) == nzl and int(line.split()[4]) == pump): #Finds that the pump and nzl has been opened and initializes the money count
                    money += float(line.split()[0])
                    continue
        with open(rs_path, 'r', errors="ignore") as rs_file:
            lines = rs_file.readlines()
            lines = lines[::-1]
            for reveresed_line in lines:#Loop from the end line to find the last closing counter of the pump and nzl and checks if it matches the total money count
                if ("Close" in reveresed_line):
                    if (int(reveresed_line.split()[2]) == nzl and int(reveresed_line.split()[3]) == pump):
                        #Money comparison with a precision of 1 digits after the decimal point
                        money = int(money*100)
                        money = float(money)/100
                        close_money_counter = float(reveresed_line.split()[0])
                        if abs(money - close_money_counter) > 1:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference of " + str(abs(money - close_money_counter)) + " in the counter")
                            return True
                        else:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has no difference in the counter")
                            return False
    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been closed" + str(money))
    return False

def dlg_finder(rs_path, DLG_path, date, pump, nzl):
    with open(rs_path, 'r', errors="ignore") as file:
        lines = file.readlines()
        reversed_lines = reversed(lines)
        for line in lines[1:]:
            if("Open" in line):#Gets the opening time of the shift from the RS file
                start_shift = line[52:56]
                break
        for line in reversed_lines:#Gets the closing time of the shift from the RS file
            if("Close" in line):
                end_shift = line[52:56]
                break
        date_obj = datetime.strptime(date[0:2] + "-" + date[2:4], '%d-%m')#changes the date format to Mar 1st format
        formatted_date = date_obj.strftime('%b %d').replace("0", " ")
        #print(formatted_date)
        temp_lines = ""
        lines_to_write = ""
        nzl_found = False
        shift_opened = False
        shift_closed = False
        for i in range(1, 30): #Loop through every DLG file with the given date and pump
            if not os.path.isfile(DLG_path + (str(i).zfill(2))): #Make sure the DLG was created
                print("Finished going through all the DLG files")
                break
            else:
                with open(DLG_path + (str(i).zfill(2)), 'r', errors="ignore") as file:
                    #print("File found")
                    i = 0
                    lines = file.readlines()
                    while (i < len(lines)):
                        if(shift_opened):
                            if("------------------------- s t a r t - p r o c e s s -------------------------" in lines[i]): #Find the start of a process
                                #print ("Process found in line " + str(i))
                                temp_lines += lines[i]
                                i += 1
                                while(i < len(lines) and "------------------------- s t a r t - p r o c e s s -------------------------" not in lines[i]): #Until next process starts
                                    if ("Handle " + str(nzl)) in lines[i]: #A flag if this is a process with the desired nzl
                                        #print ("NZL found in line " + str(i))
                                        nzl_found = True
                                    temp_lines += lines[i] #Lines stored in temporary variable in case this isn't the nzl we want
                                    if(shift_opened and formatted_date in lines[i] and "Close Shift" in lines[i]): #If the shift was close in the middle of a process
                                        #print("Shift closed in line in the middle of a process!")
                                        shift_closed = True
                                        break
                                    i += 1
                                i-=1 #This is to copy the --start process-- line for the next process and in case we exit the while loop at the end of the file
                                if nzl_found:
                                    lines_to_write += temp_lines #If this is the nzl we want, copy the lines
                                    #print("copied lines")
                                    nzl_found = False
                                temp_lines = "" #Reset the temporary variable
                        if (formatted_date in lines[i] and "Open Shift" in lines[i] and start_shift in lines[i]): #Find the start of the shift
                            #print("Shift opened in line " + str(i))
                            shift_opened = True
                        if(shift_opened and formatted_date in lines[i] and "Close Shift" in lines[i] and end_shift in lines[i]): #Find the end of the shift
                            #print("Shift closed in line " + str(i))
                            shift_closed = True
                            break
                        i += 1
                    if lines_to_write != "" and shift_closed: #If we found lines to copy
                        print ("Writing to file")
                        output_path = "C:/DDA/station/log/"
                        with open(output_path + "pump" + str(pump) + " nzl" + str(nzl) + ".txt", 'w') as new_file:
                            for line in lines_to_write:
                                # Write each line to the file with a newline at the end
                                new_file.write(line)
                                print ("Stored all the processes for the pump and nozzle in a new file")
                    if shift_opened and shift_closed:
                        print("Shift opened and closed")
                        return


date = input("Please enter the date in a format of DDMM: \n")  # Get the date from the user
shift = input("Please enter the shift in a format of A, B, C: \n")  # Get the shift from the user
#amount_pump = input("Please enter the amount of pumps in the station: ")  # Get the amount of pumps in the station from the user

#Declerations

#Windows rs_path = "C:/DDA/station/data/RS" + date + "24.D1" + shift  # The path to the RS file
#Windows DLG_path = "C:/DDA/station/log/DLG" + date + "01"  # The path to the DLG file
rs_path = "C:/DDA/station/data/RS" + date + "24.D1" + shift   # The path to the RS file
DLG_path = "C:/DDA/station/log/DLG"  # The path to the DLG file
station_path = "C:/DDA/station/STATION.prm" #The path to the station.prm file


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
                if(pump_difference(rs_path, pump, nzl)):
                    if(open_close(rs_path, pump, nzl)):
                        print("The pump and nozzle was opened and closed")
                    else:
                        print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been opened and closed properly")
                else:
                    continue
else:
    print("Couldn't find the station file in the path: " + station_path)
input()