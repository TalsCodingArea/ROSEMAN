import os

date = "1305"
pump = 11
nzl = 1
filenames = []
rs_path = "C:/DDA/station/data/RS" + date + ".D1A"   # The path to the RS file
dlg_path = "C:/DDA/station/log/DLG" + date + "." + str(pump).zfill(2) # The path to the DLG file
for i in range(1, 30):
    if os.path.isfile(dlg_path + str(i).zfill(2)):
        filenames.append(dlg_path + str(i).zfill(2))

# Open the output file in write mode
combined_dlg_path = "C:/DDA/station/log/combined_dlg" + date + "." + str(pump) + ".txt"
with open(combined_dlg_path, 'w') as outfile:
    # Iterate through list of filenames
    for name in filenames:
        # Open each file in read mode
        with open(name) as infile:
            # read the data from file and write it into output file
            outfile.write(infile.read())
        # Write a newline character after each file's data
        outfile.write("\n")

with open(rs_path, 'r', errors="ignore") as rs, open(combined_dlg_path, 'r') as combined_dlg:
    i = 1
    last_tran = -1
    for line in rs:
        if ("Open" in line and int(line.split()[3])==pump and int(line.split()[2])==nzl):
            counter = float(line.split()[1])
        elif (not ("Close" in line) and int(line.split()[4])==pump and int(line.split()[3])==nzl):
            counter += float(line.split()[1])
            tran_num = line.split()[5]
            if line.split()[1] == 0:
                fs_counter = 0
                while i < len(combined_dlg) and not (tran_num in combined_dlg[i] and "rec = " in combined_dlg[i]):
                    i += 1
                while not("------ s t a r t - p r o c e s s ------" in combined_dlg[i]) and i>=0:
                    i -= 1
                i += 1
                while not("------ s t a r t - p r o c e s s ------" in combined_dlg[i]) and i<len(combined_dlg):
                    if "OP:fs" in combined_dlg[i]:
                        fs_counter += 1
                if fs_counter == 0:
                    print("Transaction number: " + line.split()[5] + " has no OP:fs")
                else:
                    print("Transaction number: " + line.split()[5] + " has " + str(fs_counter) + " OP:fs lines")
                




