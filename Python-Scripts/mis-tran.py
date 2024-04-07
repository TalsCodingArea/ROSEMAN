import os

ws_path = "C:/Users/username/Documents/ArcGIS/Projects/ProjectName"
rs_path = "C:/Users/username/Documents/ArcGIS/Projects/ProjectName/ProjectName.gdb"


with open(ws_path, 'r') as ws:
    for i in range(40, 59):
        for line in ws:
            line.split(">")
            nzl = (line[16]).split("<")[0]
            tran = (line[18][0:4].split("<", 1)[0])
            pump = (line[20]).split("<")[0]
            fuel = (line[22]).split("<")[0]
            date = line[24][0:6] + line[24][8:10]
            time = (line[24]).split("<")[0]
            id = (line[30]).split("<")[0]
            rate = (line[64]).split("<")[0]
            qty = (line[66]).split("<")[0]
            voucher = (line[46]).split("<")[0] #If there are and complete with 0 to 7 digits
            if(tran == i):
                with open(rs_path, 'r') as rs_file:
                    money = int(float(rate) * float(qty))*100
                    money = float(money)/100
                    pump = int(pump).zfill(2)
                    write_line = f"{(str(money)).rjust(9, " ")},{"  "},{qty.rjust(10, " ")},{"  "},{nzl},{"   "},{str(pump)},{"  "},{tran.rjust(9, " ")},{"  "},{time},{" "},{date},{id},{rate},{qty},{voucher}\n"
                    rs_file.write()
