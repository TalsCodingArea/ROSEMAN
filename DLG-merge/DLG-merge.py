import os
import sys
from datetime import datetime

'''
-------------------------------FUNCTIONS DESCRIPTION-------------------------------
1. open_close
    - This function checks if a pump has been opened and closed
2. pump_difference
    - This function sums the opening counter in the pump's opening with all the transactions and compares it to the closing counter
'''
#Done
def open_close(date, shift, register, pump, nzl):
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    cnt = 0
    rs_path = "/Users/talshaubi/Documents/ROSEMAN/data/RS" + date + "24.D" + register + shift
    if not os.path.isfile(rs_path):
        print("File not found")
        return
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
def pump_difference(pump, nzl):
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


def dlg_finder(array):
    start = False
    money = 0.0
    nzl = 1 #TEMPORARY
    date = input("Enter the date (DD-MM): ")
    pump = input("Enter the pump: ")
    DLG_path = "/Users/talshaubi/Documents/ROSEMAN/log/DLG" + date + "." + str(pump).zfill(2)
    found = False
    date_obj = datetime.strptime(date[0:2] + "-" + date[2:4], '%d-%m')
    formatted_date = date_obj.strftime('%b %d').replace(" 0", " ")
    print(formatted_date)
    time = "6:20" #TEMPORARY
    temp_line = ""
    nzl_found = False
    lines_to_write = ""
    for i in range(1, 30):
        if not os.path.isfile(DLG_path + (str(i).zfill(2))):
            print("File not found")
            break
        else:
            with open(DLG_path + (str(i).zfill(2)), 'r', errors="ignore") as file:
                print("File found")
                i = 0
                lines = file.readlines()
                while (i < len(lines)):
                    if(found):
                        if("------------------------- s t a r t - p r o c e s s -------------------------" in lines[i]):
                            temp_line += lines[i]
                            i += 1
                            while(i < len(lines) and "------------------------- s t a r t - p r o c e s s -------------------------" not in lines[i]):
                                if "Handle " + nzl in lines[i]:
                                    nzl_found = True
                                temp_line += lines[i]
                                i += 1
                            if nzl_found:
                                lines_to_write += temp_line
                                nzl_found = False
                            temp_line = ""
                    if (formatted_date in lines[i] and "......... Open Shift at" in lines[i] and time in lines[i]):
                        found = True
                        continue
                    if(found and formatted_date in lines[i] and".......... Close Shift at" in lines[i]):
                        break
                    i += 1
                output_path = "/Users/talshaubi/Documents/ROSEMAN/log/"
                with open(output_path + "output.txt", 'w') as file:
                    for line in lines:
                        # Write each line to the file with a newline at the end
                        file.write(line + '\n')

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

'''
file_name = 'test.txt'
string_to_search = 'Hello'
print(check_string_in_file(file_name, string_to_search))
'''

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

'''
if __name__ == "__main__":
    func_name = sys.argv[1]   # get function name
    if func_name == "pump_difference":
        pump_difference()  # call function
'''

dlg_finder([])
