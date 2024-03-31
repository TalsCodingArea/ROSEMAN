import os

#DECLERATIONS

rs_path = "C:/DDA/station/data/RS030324.D1A"
DLG_path = "C:/DDA/station/log/DLG0303.08"
pump = 8
nzl = 1
tran_start = 45
tran_end = 52
pump_start = 38
pump_end = 40
nzl_start = 34
nzl_end = 35
tmp = -1
missing_tran = []
count = 0
start_index = 50
output_path = "/C:/DDA/station/data/"
#END OF DECLERATIONS

def retrieve_transactions(rs_path, DLG_path, pump, nzl):
    pump = 8
    nzl = 1
    tran_start = 45
    tran_end = 52
    pump_start = 38
    pump_end = 40
    nzl_start = 34
    nzl_end = 35
    tmp = -1
    missing_tran = []
    count = 0
    start_index = 50
    output_path = "/C:/DDA/station/data/"
    tran_num = 0
    with open(rs_path, 'r', errors="ignore") as file:
        rs_lines = file.readlines()
        for i in range(1, len(rs_lines)):
            if (not rs_lines[i][tran_start:tran_end].isdigit()):
                continue
            if (rs_lines[i][tran_start:tran_end].isdigit() and int(rs_lines[i][pump_start:pump_end]) == pump and int(rs_lines[i][nzl_start:nzl_end]) == nzl):
                tran_num = int(rs_lines[i][tran_start:tran_end])
            if(tmp < 0):
                tmp = tran_num +1
                continue
            elif tmp == tran_num:
                tmp+=1
                continue
            else:
                missing_tran.apppend(tmp)
                missing_tran.append(i + count)
                count += 1
                tmp += 1
    #back up the rs file
    os.rename(rs_path, rs_path + ".backup")
    #Create a new rs file
    for j in range(0, 30, 2):
        if os.path.exists(DLG_path + str(j).zfill(2)):

            with open(DLG_path + str(j).zfill(2), 'r', errors="ignore") as file:

                DLG_lines = file.readlines()
                for DLG_line in DLG_lines:
                    if ("rec =" in DLG_lines and str(missing_tran[i]) in DLG_lines):
                        source_line = DLG_line[start_index:]
                        rs_lines = rs_lines[:missing_tran[i+1]] + source_line + rs_lines[missing_tran[i+1]:]
    with open(rs_path, 'w') as new_file:

        for line in rs_lines:
            # Write each line to the file with a newline at the end
            new_file.write(line)
            print ("Stored all the processes for the pump and nozzle in a new file")

retrieve_transactions(rs_path, DLG_path, pump, nzl)
