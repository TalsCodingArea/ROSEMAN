import os

#DECLERATIONS
pos_prm_path = "C:\temp\Tal\POS.prm"
ch_path = "C:\DDA\station\CH.PRM"
proc_path = "C:\DDA\station\RFC_PROC.INI"
ini_path =  "C:\DDA\station\RFC_3000.INI"
prm_path = "C:\DDA\station\STATION.PRM"
#END DECLERATIONS


#Step 1: Check for the SMS-Print
if not os.path.isfile(pos_prm_path):
        print("POS.prm file not found")
else:
    with open(pos_prm_path, 'r', errors="ignore") as file:
        lines = file.readlines()
        for line in lines:
            if ("Sms-Print" in line):
                if line[10] == 'y':
                      print("SMS-Print is enabled")
                else:
                     line[10] = 'y'
                     os.rename(pos_prm_path, pos_prm_path + "old")
                     with open(pos_prm_path, 'w') as new_file:
                          new_file.write(lines)
                     print("Sms-Print was not enabled and now updated")
                     break


#Step 2: Check for "FUEL 4" line on the CH.PRM file
manager_flag = False
if not os.path.isfile(ch_path):
        print("CH.prm file not found")
else:
    with open(ch_path, 'r', errors="ignore") as file:
        lines = file.readlines()
        i = 0
        while (i<len(lines)):
            if ("MANAGER" in lines[i] and not manager_flag): #Checks if we are on the MANAGER section
                 manager_flag = True
            if (manager_flag and lines[i] is not ""):
                if ("FUEL4" in lines[i]):
                     print ("FUEL4 line found on the CH.PRM file")
                     break
                lines_list = lines.split('\n')
                lines_list.insert(i - 1, "210705 FUEL4")
                lines = '\n'.join(lines_list)
                os.rename(ch_path, ch_path + "old")
                with open(ch_path, 'w') as new_file:
                    new_file.write(lines)
                    print("FUEL4 line has been added")
                    break


#Step 3: Validate process 20 and rocess 30 on RFC_PROC
if not os.path.isfile(proc_path):
    print("RFC_PROC file not found")
else:
    with open(proc_path, 'r', errors='ignore') as file:
        lines = file.readlines()
        i = 0
        while i<len(lines):
            if("PROCESS 20" in lines[i]):
                i += 1
                if (lines[i].startswith("//")): #If the line after process 20 is commented
                    i += 3
                    continue
                else: #Change the lines to be commented
                    for j in range (4):
                        lines[i] = "//" + lines[i]
                        i += 1
                    print ("Added the comments for process 20")
            if ("PROCESS 30" in lines[i]):
                i += 1
                if (lines[i].startswith("//")):
                    for j in range(5):
                        lines[i] = lines[i][2:]
                        i += 1
                    print ("Removed the comment from process 30")
                    break
                break
        os.rename(proc_path, proc_path + "old")
        with open(proc_path, 'w') as new_file:
            new_file.write(lines)
            print("Modified the PROC file")


#Step 4: validate the RFC_3000
if not os.path.isfile(ini_path):
    print("RFC_3000 file not found")
else:
    with open(ini_path, 'r', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            if(line.startswith("Company")):
                if ("fuel4" in line):
                    print("fuel4 line found on RFC_3000 file")
                    break
                else:
                    line += ",fuel4"
                    print("Added 'fuel4' to Company line on RFC_3000 file")
                    break
        os.rename(ini_path, "old RFC_3000")
        with open(ini_path, 'w') as new_file:
            new_file.write(lines)
            print("RFC_3000 file done")



#Step 5: Validate STATION.PRM
'''if not os.path.isfile(prm_path):
    print("STATION.PRM file not found")
else:
    with open(prm_path, 'r', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            if (not (line.Substring(73, 75) is "\d")):
                print "line " + str()'''