import os
import re

rs_path = "C:/temp/Dif/RS040524.D1A"  # The path to the RS file
DLG_path = "C:/temp/Dif/DLG2804.06"  # The path to the DLG file
station_path = "C:/temp/Dif/STATION.PRM" #The path to the station.prm file
dlg_folder_path = "C:/temp/Dif/Tal/DLG1504.03"

#End of declerations
def tran_check(rs_path, dlg_path, pump, nzl):
    if not os.path.isfile(rs_path):
        print("RS file not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            first_line = True
            cnt = 0.0 #This is the counter for the liters in the pump and nzl
            dlg = []
            for i in range (1, 30):
                if not os.path.isfile(dlg_path + (str(i).zfill(2))):
                    break
                else:
                    with open(dlg_path + (str(i).zfill(2)), 'r', errors='ignore') as dlg_file:
                        for line in dlg_file:
                            dlg.append(line)
            for line in rs_file:
                time = ""
                shift_opened = False
                if first_line:
                    first_line = False
                    continue
                if ("Open" in line and int(line.split()[3]) == pump and int(line.split()[2]) == nzl):
                    cnt = float(line.split()[1])
                    time = line.split()[5]
                if (line.split()[5].isdigit() and int(line.split()[4]) == pump and int(line.split()[3]) == nzl):
                    tran_num = line.split()[5]
                    print(line[:70])
                    dlg_path = dlg_path[:-3]
                    op_fs_cnt = 0
                    for i in range(len(dlg)):
                        if("Handle 3" in dlg[i]):
                            print(dlg[i][:6])
                        if ("rec =" in dlg[i] and tran_num in dlg[i]):
                            start_process = False
                            invalid_cnt = 0
                            while not start_process and i > 0:
                                i -= 1
                                if ("- s t a r t - p r o c e s s -" in dlg[i]):
                                    start_process = True
                                    i += 1
                            while start_process and i < len(dlg):
                                if ("- s t a r t - p r o c e s s -" in dlg[i]):
                                    if(float(op_fs_cnt) > float(line.split()[1])):
                                        print("The transaction number " + tran_num + " pumped fuel and not registered correctly")
                                    if (invalid_cnt > 10):
                                        print("Found several lines with 'Invalid event' on the process description of transaction number: " + tran_num)
                                    cnt += float(line.split()[1])
                                    break
                                if ("Current  total volume=" in dlg[i]):
                                    current = float(extract_between(dlg[i]))
                                    if (abs(current - cnt) > 1):
                                        print("The opening counter for transaction number " + tran_num + " is not equal to the sum of the earlier transactions")
                                        return
                                if ("OP:fs" in dlg[i]):
                                    op_fs_cnt += 1
                                if (re.search('Dda: .*.  F' + str(pump).zfill(2), dlg[i])):
                                    tmp = cnt + float(line.split()[1])
                                    if (abs(tmp - float(dlg[i][-9:])) > 1):
                                        print("The transaction number " + tran_num + " is correct")
                                        break
                                    else:
                                        print("Transaction number: " + tran_num + " is not correcrt")
                                if ("Invalid" in dlg[i]):
                                    invalid_cnt += 1
                                i += 1
                            cnt += float(line.split()[1])
                            break
    return False

def pump_difference(rs_path, pump, nzl):
    first_line = True
    counter = 0.0
    if not os.path.isfile(rs_path):
        print("RS file not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as rs_file:
            for line in rs_file:#Sum the counter starting count with all the transactions
                if first_line:
                    first_line = False
                    continue
                if "Open" in line:
                    if(int(line.split()[2]) == nzl and int(line.split()[3]) == pump and counter == 0): #This is the first open for the pump and nzl
                        counter = float(line.split()[1])
                    elif(int(line.split()[2]) == nzl and int(line.split()[3]) == pump and counter != 0): #This is not the first opening for the pump and nzl so we compare the counter counter
                        if(abs(counter - float(line.split()[1])) > 1):
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference in the counter of " + str(abs(counter - float(line.split()[1]))) + " before the opening at " + line.split()[5])
                            return False
                elif ("Close" not in line and int(line.split()[3]) == nzl and int(line.split()[4]) == pump): #Finds that the pump and nzl has been opened and initializes the counter count
                    counter += float(line.split()[1])
                    continue
        with open(rs_path, 'r', errors="ignore") as rs_file:
            lines = rs_file.readlines()
            lines = lines[::-1]
            for reveresed_line in lines:#Loop from the end line to find the last closing counter of the pump and nzl and checks if it matches the total counter count
                if ("Close" in reveresed_line):
                    if (int(reveresed_line.split()[2]) == nzl and int(reveresed_line.split()[3]) == pump):
                        #counter comparison with a precision of 1 digits after the decimal point
                        counter = int(counter*10)
                        counter = float(counter)/10
                        close_counter_counter = float(reveresed_line.split()[1])
                        close_counter_counter = int(close_counter_counter*10)
                        close_counter_counter = float(close_counter_counter)/10
                        if abs(counter - close_counter_counter) > 1:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has a difference of " + str(abs(counter - close_counter_counter)) + " in the counter")
                            return True
                        else:
                            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has no difference in the counter")
                            return False
    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been closed" + str(counter))
    return False
                                                  
def extract_between(s):
    start = s.find('=') + 1 # to get the index after "="
    end = s.find(';') # to get the index of ";"
    return s[start:end].strip() if start != -1 and end != -1 else "Not found" # strip to remove leading/trailing spaces


#tran_check("C:/temp/Dif/RS170424.D1B", "C:/temp/Dif/DLG1704.01", 1, 1)

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
                else:
                    continue
else:
    print("Couldn't find the station file in the path: " + station_path)


tran_check(rs_path, DLG_path, 3, 3)