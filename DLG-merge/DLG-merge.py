import os
import sys


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
            elif (int(line[pump_start:pump_end].replace(" ", "")) == pump and line[tran_start:tran_end].replace(" ", "").isdigit() and start):
                money += float(line[0:6].replace(" ", ""))
        for reveresed_line in reversed(lines):
            if (int(reveresed_line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) and reveresed_line[tran_start:tran_end].replace(" ", "") == "Close"):
                return (money == float(reveresed_line[money_start:money_end].replace(" ", "")))
    print("Pump: " + pump + " NZL: " + nzl + " has been opened and not closed")
    return False

def dlg_finder(array):
    for i in range(len(array)):
        if array[i] == "DLG":
            return i
    return -1



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


if __name__ == "__main__":
    func_name = sys.argv[1]   # get function name
    if func_name == "pump_difference":
        pump_difference()  # call function

pump_difference(1, 1)