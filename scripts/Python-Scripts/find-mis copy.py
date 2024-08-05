import os

#DECLERATIONS

rs_path = "C:/DDA/station/data/RS060324.D1B"
DLG_path = "C:/DDA/station/log/DLG0603.07"
pump = 7
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
    tran_start = 45
    tran_end = 51
    tmp = -1
    start_index = 39
    new_rs_path = rs_path[:-3] + "BACKUP"
    tran_num = 0
    first_line = True
    with open(rs_path, 'r', encoding='utf8') as rs, open(new_rs_path, 'w', encoding='utf8') as new_rs:
        for line in rs:
            if first_line:
                first_line = False
                new_rs.write(line)
                continue
            if (not line[tran_start:tran_end].isdigit()):#Skip all the lines that doesn't have transaction number in them
                new_rs.write(line)
                continue
            else:
                tran_num = int(line[tran_start:tran_end].replace(" ", ""))
            if(tmp < 0):
                tmp = tran_num + 1
                new_rs.write(line)
                continue
            elif tmp == tran_num:
                new_rs.write(line)
                tmp += 1
                continue
            else:
                cnt = tran_num - tmp
                while(cnt>0):
                    for i in range(1, 30):
                        if os.path.exists(DLG_path + str(i).zfill(2)):
                            with open(DLG_path + str(i).zfill(2), 'r', errors='ignore') as file:
                                for DLG_line in file:
                                    if("rec =" in DLG_line and str(tmp) in DLG_line):
                                        new_rs.write(DLG_line[start_index:])
                                        i = 30
                    cnt -= 1
                tmp = tran_num + 1
                new_rs.write(line)

retrieve_transactions(rs_path, DLG_path, pump, nzl)
