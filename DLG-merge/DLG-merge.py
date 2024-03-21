import os
import sys


def counter_difference():
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    date = input("Enter the date (DD-MM): ")
    shift = input("Enter the shift (A, B, C): ")
    register = input("Enter the register number: ")
    rs_path = "/Users/talshaubi/Documents/GitHub/ROSEMAN/data/RS" + date + "24.D" + register + shift
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
    if func_name == "counter_difference":
        counter_difference()  # call function