import os
import sys
from datetime import datetime

'''
-------------------------------FUNCTIONS DESCRIPTION-------------------------------
1. open_close
    - This function checks if a pump has been opened and closed
2. pump_difference
    - This function sums the opening counter in the pump's opening with all the transactions and compares it to the closing counter
3. dlg_finder
    - This function finds all the processes of a pump and nzl in a given shift
    @param array: An array of the following format: [nzl, start_shift, end_shift, date, pump, nzl, start_shift, end_shift, date, pump, ...]
    The time should be in the format of 20:30
    The date should be in the format of 0103 (Mar 1st)
    @return: A file with all the processes of the given pump and nzl in the given shift called output.txt
'''
#Done
def open_close(rs_path, pump, nzl):
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    cnt = 0
    if not os.path.isfile(rs_path):
        #print("File not found")
        return False
    else:
        with open(rs_path, 'r', errors="ignore") as file:
            lines = file.readlines()
            reversed_lines = reversed(lines)
        for line in lines[1:]:
            if (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) == nzl and line[tran_start:tran_end].replace(" ", "") == "Open"):
                cnt += 1
            elif (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) == nzl and line[tran_start:tran_end].replace(" ", "") == "Close"):
                cnt -= 1
    if cnt == 0:
        print("Pump: " + pump + " NZL: " + nzl + " has been opened and closed")
        return True
    elif cnt > 0:
        print("Pump: " + pump + " NZL: " + nzl + " has been opened and not closed")
        return False
    else:
        print("Pump: " + pump + " NZL: " + nzl + " has been closed more times than opened")
        return False

#Done
def pump_difference(rs_path, pump, nzl):
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    money_start = 0
    money_end = 9
    start = False
    money = 0.0
    if not os.path.isfile(rs_path):
        print("File not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as file:
            lines = file.readlines()
            reversed_lines = reversed(lines)
        for line in lines[1:]:
            if (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) and line[tran_start:tran_end].replace(" ", "") == "Open" and not start):
                money = float(line[money_start:money_end].replace(" ", ""))
                start = True
                continue
            elif (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) == nzl and line[tran_start:tran_end].replace(" ", "").isdigit() and start):
                money += float(line[money_start:money_end].replace(" ", ""))
        for reveresed_line in reversed(lines):
            if (int(reveresed_line[pump_start:pump_end].replace(" ", "")) == pump and int(reveresed_line[nzl_start:nzl_end].replace(" ", "")) == nzl and reveresed_line[tran_start:tran_end].replace(" ", "") == "Close"):
                money = int(money*100)
                money = float(money)/100
                return (money == float(reveresed_line[money_start:money_end].replace(" ", "")))
    print("Pump: " + pump + " NZL: " + nzl + " has been opened and not closed")
    return False

#Done
def dlg_finder(rs_path, DLG_path, date, pump, nzl):
    with open(rs_path, 'r', errors="ignore") as file:
        lines = file.readlines()
        reversed_lines = reversed(lines)
        for line in lines[1:]:
            if("Open" in line):
                start_shift = line[45:51]
                break
        for line in reversed_lines:
            if("Close" in line):
                end_shift = line[45:51]
                break
        date_obj = datetime.strptime(date[0:2] + "-" + date[2:4], '%d-%m')
        formatted_date = date_obj.strftime('%b %d').replace("0", " ")
        #print(formatted_date)
        temp_lines = ""
        lines_to_write = ""
        nzl_found = False
        shift_opened = False
        shift_closed = False
        for i in range(1, 30): #Loop through every DLG file with the given date and pump
            if not os.path.isfile(DLG_path + (str(i).zfill(2))): #Make sure the DLG was created
                print("File not found")
                break
            else:
                with open(DLG_path + (str(i).zfill(2)), 'r', errors="ignore") as file:
                    print("File found")
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
                                        print ("NZL found in line " + str(i))
                                        nzl_found = True
                                    temp_lines += lines[i] #Lines stored in temporary variable in case this isn't the nzl we want
                                    if(shift_opened and formatted_date in lines[i] and "Close Shift" in lines[i]): #If the shift was close in the middle of a process
                                        print("Shift closed in line in the middle of a process!")
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
                        if(shift_opened and formatted_date in lines[i] and "Close Shift" in lines[i] and end_shift in line[i]): #Find the end of the shift
                            #print("Shift closed in line " + str(i))
                            shift_closed = True
                            break
                        i += 1
                    if lines_to_write != "" and shift_closed: #If we found lines to copy
                        print ("Writing to file")
                        output_path = "/Users/talshaubi/Documents/ROSEMAN/log/"
                        with open(output_path + "pump " + pump + " nzl " + nzl + ".txt", 'w') as new_file:
                            for line in lines_to_write:
                                # Write each line to the file with a newline at the end
                                new_file.write(line)
                    if shift_opened and shift_closed:
                        print("Shift opened and closed")
                        return

def check_string_in_file(file_name, string_to_search):
    """Check if any line in the file contains given string."""
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if string is present
            if string_to_search in line:
                return True
    return False

def counter_difference():
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    money_start = 0
    money_end = 6
    date = input("Enter the date (DD-MM): ")
    shift = input("Enter the shift (A, B, C): ")
    register = input("Enter the register number: ")
    rs_path = "/Users/talshaubi/Documents/ROSEMAN/data/RS" + date + "24.D" + register + shift
    if not os.path.isfile(rs_path):
        print("File not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as file:
            lines = file.readlines()
            reversed_lines = reversed(lines)
        for line in lines[1:]:
            tran_val = line[tran_start:tran_end].replace(" ", "")
            if not tran_val.isdigit():
                pump_number = line[pump_start:pump_end]
                nzl_number = line[nzl_start:nzl_end]
                for reveresed_line in reversed(lines):
                    trans_val = reveresed_line[tran_start:tran_end].replace(" ", "")
                    if not trans_val.isdigit():
                        if(reveresed_line[pump_start:pump_end] == pump_number and reveresed_line[nzl_start:nzl_end] == nzl_number):
                            if trans_val == "Close":
                                print("Pump: " + pump_number + " NZL: " + nzl_number + " has been opened and closed")
                                break
                        else:
                            continue
                    else:
                        print("Pump: " + pump_number + " NZL: " + nzl_number + " has been opened and not closed after the last transaction")
                        break
            else:
                print("Finished going through the file")
                break
    return


date = input("Please enter the date in a format of DDMM: ")  # Get the date from the user
shift = input("Please enter the shift in a format of A, B, C: ")  # Get the shift from the user
amount_pump = input("Please enter the amount of pumps in the station: ")  # Get the amount of pumps in the station from the user
rs_path = "/Users/talshaubi/Documents/ROSEMAN/data/RS" + date + "24.D1" + shift  # The path to the RS file

for i in range(1, 3): #Loop through all the registers
    if os.path.isfile(rs_path):
        for j in range(1, int(amount_pump) + 1): #Loop through all the pumps
            DLG_path = "/Users/talshaubi/Documents/ROSEMAN/log/DLG" + date + str(j).zfill(2)  # The path to the DLG file
            for t in range(1, 4): #Loop through all the NZLs
                if(pump_difference()):
                    print("Pump: " + j + " NZL: " + t + " has a difference in the counter")
                    if(open_close(rs_path, j, t)):
                        print("Pump: " + j + " NZL: " + t + " has been opened and closed")
                        dlg_finder([t, shift, shift, date, j])
                    else:
                        print("Pump: " + j + " NZL: " + t + " has not been opened and closed properly")
                else:
                    continue
print("Done :)")