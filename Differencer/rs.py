import os
import datetime
import func
import pandas as pd

dict = func.get_dict()

def next_rs(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    new_rs_path = rs_path[:-1] + (chr(ord(rs_path[-1]) + 1)).upper()
    # Check if the next RS is on the same day
    if os.path.exists(new_rs_path):
        return new_rs_path
    # If not, check if the next RS is on the next day
    rs_date = rs_path.split('RS')[1][:4]
    new_rs_date = func.get_next_day(rs_date)
    new_rs_path = rs_path.replace(rs_date, new_rs_date)[:-1] + 'A'
    if os.path.exists(new_rs_path):
        return new_rs_path
    # If there is no next RS, return 0
    return 0
    
def get_opened_pumps(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    pumps_set = set()
    with open(rs_path, 'r', errors='ignore') as rs:
        for line in rs:
            if 'Open' in line:
                pumps_set.add(line[dict['PUMP']['start']:dict['PUMP']['end']].strip())
    return pumps_set

def get_closed_pumps(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    pumps_set = set()
    with open(rs_path, 'r', errors='ignore') as rs:
        for line in rs:
            if 'Close' in line:
                pumps_set.add(line[dict['PUMP']['start']:dict['PUMP']['end']].strip())
    return pumps_set

def check_pumps_open_closed(rs_path):
    return get_opened_pumps(rs_path) - get_closed_pumps(rs_path)

def get_pumps_nzl(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    pumps_set = set()
    pumps_array = []
    with open(rs_path, 'r', errors='ignore') as rs:
        for line in rs:
            pumps_set.add(line[dict['PUMP']['start']:dict['PUMP']['end']].strip())
        for pump in pumps_set:
            if 'NZL' in line:
                pumps_set.add(pump)
    return pumps_array

def get_pumps_diff(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    pumps_dict = {}
    diff_array = []
    with open(rs_path, 'r', errors='ignore') as rs:
        lines = rs.readlines()
        # For each line in the RS let's add the pumps and sum the counters
        for line in lines:
            if 'MONEY' in line:
                continue
            pump = line[dict['PUMP']['start']:dict['PUMP']['end']].strip()
            nzl = line[dict['NZL']['start']:dict['NZL']['end']].strip()
            count = float(line[dict['QTY']['start']:dict['QTY']['end']].replace(' ', ''))
            if pump in pumps_dict:
                if nzl in pumps_dict[pump]:
                    if not ('Open' in line or 'Close' in line):
                        pumps_dict[pump][nzl]['count'] += count
                else:
                    pumps_dict[pump][nzl] = {
                        'open' : count,
                        'close' : -1.0,
                        'count' : 0.0
                    }
            else:
                pumps_dict[pump] = {
                    nzl : {
                        'open' : count,
                        'close' : -1.0,
                        'count' : 0.0
                    }
                }
        # Let's find the last 'Close' for each pump and nzl
        reversed_lines = lines[::-1]
        for reveresed_line in reversed_lines:
            if 'Close' in reveresed_line:
                pump = reveresed_line[dict['PUMP']['start']:dict['PUMP']['end']].strip()
                nzl = reveresed_line[dict['NZL']['start']:dict['NZL']['end']].strip()
                count = float(reveresed_line[dict['QTY']['start']:dict['QTY']['end']].replace(' ', ''))
                if pump in pumps_dict and nzl in pumps_dict[pump] and pumps_dict[pump][nzl]['close'] == -1:
                    pumps_dict[pump][nzl]['close'] = count
        # Let's check if there are any differences
        for pump in pumps_dict:
            for nzl in pumps_dict[pump]:
                if  abs((pumps_dict[pump][nzl]['open'] + pumps_dict[pump][nzl]['count']) - pumps_dict[pump][nzl]['close']) > 1:
                    diff_array.append([pump, nzl, round(pumps_dict[pump][nzl]['open'] + pumps_dict[pump][nzl]['count'] - pumps_dict[pump][nzl]['close'], 2)])
    return diff_array
                    
def neg_diff(pump, nzl, rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        for line in rs:
            if 'MONEY' in line:
                continue
            if pump == line[dict['PUMP']['start']:dict['PUMP']['end']].strip() and nzl == line[dict['NZL']['start']:dict['NZL']['end']].strip():
                return float(line[dict['QTY']['start']:dict['QTY']['end'].replace(' ', '')])
    return 0

def pos_diff(pump, nzl, rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        for line in rs:
            if 'MONEY' in line:
                continue
            if pump == line[dict['PUMP']['start']:dict['PUMP']['end']].strip() and nzl == line[dict['NZL']['start']:dict['NZL']['end']].strip():
                return float(line[dict['QTY']['start']:dict['QTY']['end'].replace(' ', '')])
    return 0

def close_pump(pump, rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        lines = rs.readlines()
        reversed_lines = lines[::-1]
        for reveresed_line in reversed_lines:
            if 'Close' in reveresed_line:
                close_timedate = reveresed_line[dict['TIME']['start']:dict['DATE']['end']].strip()
                break
    done = False
    next_rs_path = next_rs(rs_path)
    lines_to_copy = []
    while not done and next_rs_path != 0:
        with open(next_rs_path, 'r', errors='ignore') as rs:
            found = False
            for line in rs:
                if 'MONEY' in line:
                    continue
                if found:
                    if pump == line[dict['PUMP']['start']:dict['PUMP']['end']].strip():
                        lines_to_copy.append(line)
                    else:
                        done = True
                        break
                elif pump == line[dict['PUMP']['start']:dict['PUMP']['end']].strip():
                    found = True
                    lines_to_copy.append(line)
        next_rs_path = next_rs(next_rs_path)
    for line in lines_to_copy:
        line_to_write = func.open_to_close(line, close_timedate)
        with open(rs_path, 'a', errors='ignore') as rs:
            rs.write(line_to_write)

def rs_to_excel(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    rs_extension = rs_path.split('.D1')[-1]
    excel_file_path = rs_path.replace('.D1' + rs_extension, '.xlsx')
    with open(rs_path, 'r', errors='ignore') as file:
        lines = file.readlines()

    headers, indices = func.parse_headers()
    data = func.parse_data(lines[1:], indices)

    # Create a DataFrame and write to Excel
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(excel_file_path, index=False)

def ps_to_excel(ps_path):
    # Safety that this is a valid RS path
    if not os.path.exists(ps_path):
        return 0
    ps_extension = ps_path.split('.D1')[-1]
    excel_file_path = ps_path.replace('.D1' + ps_extension, '.xlsx')
    with open(ps_path, 'r', errors='ignore') as ps:
        lines = ps.readlines()

    headers, indices = func.parse_headers()
    data = func.parse_data(lines[1:], indices)

    # Create a DataFrame and write to Excel
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(excel_file_path, index=False)

def folder_to_excel(folder_path):
    file_names = os.listdir(folder_path)
    headers, indices = func.parse_headers()
    data = []
    for file_name in file_names:
        if 'RS' in file_name:
            rs_path = folder_path + file_name
            if not os.path.exists(rs_path):
                continue
            with open(rs_path, 'r', errors='ignore') as rs:
                lines = rs.readlines()
                data.append(func.parse_data(lines[1:], indices))
        if 'PS' in file_name:
            ps_path = folder_path + file_name
            if not os.path.exists(ps_path):
                continue
            with open(ps_path, 'r', errors='ignore') as ps:
                lines = ps.readlines()
                data.append(func.parse_data(lines[1:], indices))
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(folder_path + 'data.xlsx', index=False)

def get_headers(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        headers = rs[0].split()
        return headers
    
def get_indices(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        header_line = rs[0]
        headers, indices = func.parse_headers(header_line)
        return indices

def double_rs_safety(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        lines = rs.readlines()
        for line in lines:
            if 'Close' in line:
                return rs_path
        next_rs = next_rs(rs_path)
        with open(next_rs, 'r', errors='ignore') as next_rs, open(rs_path.replace('RS', 'combined_rs'), 'w') as combined_rs:
            combined_rs.write(rs.read())
            lines = next_rs.readlines()
            for line in lines[1:]:
                combined_rs.write(line)
        return rs_path.replace('RS', 'combined_rs')

def get_open_close(rs_path):
    # Safety that this is a valid RS path
    if not os.path.exists(rs_path):
        return 0
    with open(rs_path, 'r', errors='ignore') as rs:
        lines = rs.readlines()
        for line in lines:
            if 'Open' in line:
                open_timedate = line[dict['TIME']['start']:dict['DATE']['end']].strip()
                break
        for line in reversed(lines):
            if 'Close' in line:
                close_timedate = line[dict['TIME']['start']:dict['DATE']['end']].strip()
                break
        return open_timedate, close_timedate
