import os
import re
from datetime import datetime


'''
-------------------------------FUNCTIONS DESCRIPTION-------------------------------
1. open_close
    @param rs_path: The path to the RS file. STRING
    @param pump: The pump number. INTEGER
    @param nzl: The nzl number. INTEGER
    @return: True if the pump has been opened and closed the same amount of times, False otherwise
    - This function runs through the entire RS file and checks if the number of times a pump has been opened and closed
    - If the numbers match it will return True
    #If the rs path is not found, will return False

2. pump_difference
    @param rs_path: The path to the RS file. STRING
    @param pump: The pump number. INTEGER
    @param nzl: The nzl number. INTEGER
    @return: True if the pump's closing money counter is equal to the pump's opening counter with all the transactions, False otherwise
    - The function loop through the rs file lines until it find the pump and nzl opening line, initializes the money count and sums all the transactions after the opening
    - Once done the sum of the money counter is compared to the last closing counter of the pump and nzl
    #This function is reffering to the money counter only
    #The comparison between the sum of the transactions and the last closing counter is done with a precision of 1 digits after the decimal point
    #If the rs path is not found, will return Null
    #If the pump and nzl has not been opened, will return False

3. dlg_finder
    @param rs_path: The path to the RS file. STRING
    @param DLG_path: The path to the DLG file not including the last 2 digits of the log number. STRING
    @param date: The date of the shift. STRING
    @param pump: The pump number. INTEGER
    @param nzl: The nzl number. INTEGER
    @return: Creates a file with the DLG processes of the pump and nzl in the given date and shift
    - The function start by going to the RS file and finding the opening and closing time of the shift
    - Once the shift time is found, the function goes through all the DLG files with the given date and pump
    - If there is a process with the given pump and nzl, the function will copy the process to a new file
    #This function
'''


#Done
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

#Done
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
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference in the counter of " + str(abs(money - float(line.split()[0]))) + " before the opening at " + line.split()[5])
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
                        money = int(money*10)
                        money = float(money)/10
                        close_money_counter = float(reveresed_line.split()[0])
                        close_money_counter = int(close_money_counter*10)
                        close_money_counter = float(close_money_counter)/10
                        if abs(money - close_money_counter) > 1:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference of " + str(abs(money - close_money_counter)) + " in the counter")
                            return True
                        else:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has no difference in the counter")
                            return False
    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been closed" + str(money))
    return False

#Done
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

def dlg_check(rs_path, DLG_path, pump, nzl):
    if not os.path.isfile(rs_path):
        print("RS file not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            tran_array = []
            money = 0.0
            for line in rs_file:
                if("Open" in line and money == 0):
                    money = float(line.split()[0])
                if (line.split()[5].isdigit() and int(line.split()[3]) == pump and int(line.split()[2]) == nzl):
                    tran_array.append(line)
            for tran in tran_array:
                open_process = False
                handle = False
                tran_num = False
                handle_closed = False
                cnt = 0
                counter_match = False
                money += float(tran.split()[0])
                for i in range(1, 30):
                    if not (os.path.isfile(DLG_path + (str(i).zfill(2))) and os.path.isfile(rs_path)):
                        open_process = False
                        break
                    else:
                        with open(DLG_path + (str(i).zfill(2)), 'r', errors="ignore") as DLG_file:
                            for line in DLG_file:
                                if ("- s t a r t - p r o c e s s -" in line):
                                    open_process = True
                                else:
                                    if(str(money)[:-2] in line):
                                        print("All the transaction until " + tran.split()[5] + " are correct")
                                    if("Handle " + str(nzl) in line):
                                        handle = True
                                    if(tran.split()[5] in line):
                                        tran_num = True
                                    if("Handle 0" and handle):
                                        handle_closed = True
                                    if(handle and not handle_closed):
                                        if ("OP:fs" in line):
                                            cnt += 1

def tran_check(rs_path, DLG_path, pump, nzl):
    if not os.path.isfile(rs_path):
        print("RS file not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            for line in rs_file:
                first_line = True
                for line in rs_file:
                    cnt = 0.0
                    time = ""
                    shift_opened = False
                    if first_line:
                        first_line = False
                        continue
                    if (line.split()[5] == "Open" and int(line.split()[3]) == pump and int(line.split()[2]) == nzl):
                        cnt = line.split()[1]
                        time = line.split()[5]
                    if (line.split()[5].isdigit() and int(line.split()[4]) == pump and int(line.split()[3]) == nzl):
                        tran_num = line.split()[5]
                        DLG_path = DLG_path[:-3]
                        for i in range (1, 30):
                            if not os.path.isfile(DLG_path + (str(i).zfill(2))):
                                break
                            else:
                                with open(DLG_path + (str(i).zfill(2)), 'r', errors="ignore") as DLG_file:
                                    for i in range(len(DLG_file)):
                                        op_fs_cnt = 0
                                        if ("rec =" in DLG_file[i] and tran_num in DLG_file[i]):
                                            start_process = False
                                            invalid_cnt = 0
                                            while not start_process and i > 0:
                                                i -= 1
                                                if ("- s t a r t - p r o c e s s -" in DLG_file[i]):
                                                    start_process = True
                                                    i += 1
                                            while start_process and i < len(DLG_file):
                                                if ("- s t a r t - p r o c e s s -" in DLG_file[i]):
                                                    if(op_fs_cnt > int(line.split()[1])):
                                                        print("The transaction number " + tran_num + " pumped fuel and not registered correctly")
                                                    if (invalid_cnt >10):
                                                        print("Found several lines with 'Invalid event' on the process description of transaction number: " + tran_num)
                                                    cnt += line.split()[1]
                                                    break
                                                if ("Current  total volume=" in DLG_file[i]):
                                                    current = float(extract_between(DLG_file[i]))
                                                    if (abs(current - cnt) > 1):
                                                        print("The opening counter for transaction number " + tran_num + " is not equal to the sum of the earlier transactions")
                                                        return
                                                if ("OP:fs" in DLG_file[i]):
                                                    op_fs_cnt += 1
                                                if ("Dda: 2-1  F" in DLG_file[i]):
                                                    tmp = cnt + (line.split()[1])
                                                    tmp = int(tmp*10)
                                                    tmp = float(tmp)/10
                                                    if (str(tmp) in DLG_file[i]):
                                                        print("The transaction number " + tran_num + " is correct")
                                                        break
                                                    else:
                                                        print("Transaction number: " + tran_num + "")
                                                if ("Invalid" in DLG_file[i]):
                                                    invalid_cnt += 1
                                                i += 1
                                                    

                                                


def extract_between(s):
    start = s.find('=') + 1 # to get the index after "="
    end = s.find(';') # to get the index of ";"
    return s[start:end].strip() if start != -1 and end != -1 else "Not found" # strip to remove leading/trailing spaces







#date = input("Please enter the date in a format of DDMM: ")  # Get the date from the user
#shift = input("Please enter the shift in a format of A, B, C: ")  # Get the shift from the user
#amount_pump = input("Please enter the amount of pumps in the station: ")  # Get the amount of pumps in the station from the user

#Declerations

#Windows rs_path = "C:/DDA/station/data/RS" + date + "24.D1" + shift  # The path to the RS file
#Windows DLG_path = "C:/DDA/station/log/DLG" + date + "01"  # The path to the DLG file
#Mac rs_path = "/Users/talshaubi/Documents/ROSEMAN/data/RS" + date + "24.D1" + shift  # The path to the RS file
#Mac DLG_path = "/Users/talshaubi/Documents/ROSEMAN/log/DLG" + date + "01"  # The path to the DLG file

rs_path = "C:/temp/Dif/RS150424.D1A"   # The path to the RS file
DLG_path = "C:/DDA/station/log/DLG"  # The path to the DLG file
station_path = "C:/temp/Dif/STATION.prm" #The path to the station.prm file

#End of declerations


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
                    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference in the counter")
                    print("Looking if the pump and nozzle was opened and closed properly...")
                    if(open_close(rs_path, pump, nzl)):
                        print("The pump and nozzle was opened and closed")
                        DLG_path += "." + str(pump).zfill(2)  # The path to the DLG file
                        #print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has been opened and closed")
                        #dlg_finder(rs_path, DLG_path, pump, nzl)
                        #DLG_path = DLG_path[:-3]
                    else:
                        print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been opened and closed properly")
                else:
                    continue
else:
    print("Couldn't find the station file in the path: " + station_path)
#input()