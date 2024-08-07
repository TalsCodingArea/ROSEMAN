import func
import os
import rs

dict = func.get_dict()

print("Hello, welcome to the Differencer program!")
date = input("Press Enter the date of the RS file in the format of DDMM: \n")
rs_path = "C:\\Users\\tals\\Documents\\GitHub\\ROSEMAN\\data\\data\\RS" + date + '24.D1A'
rs_path = rs.double_rs_safety(rs_path)

while os.path.exists(rs_path) and rs_path[-10:-6] == date:
    pumps_to_close = rs.check_pumps_open_closed(rs_path)
    if len(pumps_to_close) > 0:
        print("The following pumps are still open: ", pumps_to_close)
        ans = input("Would you like me to close them for you?\n")
        if ans.lower() == 'y' or ans.lower() == 'yes':
            for pump in pumps_to_close:
                rs.close_pump(pump, rs_path)
    diff_array = rs.get_pumps_diff(rs_path)
    if diff_array:
        for diff in diff_array:
            ans = input("Found difference in pump: " + diff[0] + ", nzl: " + diff[1] + ". Would you like to find it?\n")
            if ans.lower() == 'y' or ans.lower() == 'yes':
                rs.pos_diff(diff[0], diff[1], rs_path) if diff[2] > 0 else rs.neg_diff(diff[0], diff[1], rs_path)
    rs_path = rs_path[:-1] + (chr(ord(rs_path[-1]) + 1)).upper()