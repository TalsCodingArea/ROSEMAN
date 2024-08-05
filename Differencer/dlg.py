import os
import func
import datetime
import rs

dict = func.get_dict()

def combine_dlg(pump, rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    date = rs_path[-10:-6]
    dlg_path = 'C:\\DDA\station\\log\\DLG' + date + '.' + pump
    combined_dlg_path = dlg_path.replace('DLG', 'COMBINED_DLG')
    open_timedate, close_timedate = rs.get_open_close(rs_path)
    open_date = datetime.strptime(open_timedate.split()[1], "%d/%m/%y")
    formatted_open_date = open_date.strftime("%a %b %-d")
    open_line = 'Open Shift at ' + formatted_open_date
    close_date = datetime.strptime(close_timedate.split()[1], "%d/%m/%y")
    formatted_close_date = close_date.strftime("%a %b %-d")
    close_line = 'Close Shift in CloseShift at ' + formatted_close_date
    with open(combined_dlg_path, 'w', errors='ignore') as combined_dlg:
        flag = False
        if open_date == close_date:
            for i in range(30):
                with open(dlg_path + str(i).zfill(2), 'r', errors='ignore') as dlg:
                    for line in dlg:
                        if flag and close_line:
                            return
                        if not flag and open_line:
                            flag = True
                            continue
                        if flag:
                            combined_dlg.write(line)
    return combined_dlg_path         

            