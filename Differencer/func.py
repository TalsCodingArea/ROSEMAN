import os
from datetime import datetime,timedelta
import pandas as pd

def get_next_day(date_str):
    # Parse the input date string
    date = datetime.strptime(date_str, "%d%m")
    
    # Add one day
    next_day = date + timedelta(days=1)
    
    # Format the date back to 'DDMM' format
    next_day_str = next_day.strftime("%d%m")
    
    return next_day_str

def get_dict() -> dict:
    headers_line = "MONEY      QTY         CAR        NZL PUMP   TRAN   TIME  DATE     FUEL       F.T  PAYMENT   CODE   ID                  ADD    WORKER  ODO      CHSPEC   RATE    DISCNT  DT   CT     CLUB                VOUCHER ST MS SNUM CUST_ID   AS CHECK_SUM NUM_CHECKS"
    headers = headers_line.split()
    headers_dict = {}
    for i, header in enumerate(headers):
        start_index = headers_line.index(header)
        if i< len(headers) - 1:
            end_index = headers_line.index(headers[i+1]) - 1
        else:
            end_index = start_index + 1
        
        headers_dict[header] = {'start': start_index, 'end': end_index}
    return headers_dict

def convert_date(ddmm):
    # Parse the input string as a date object
    date_obj = datetime.strptime(ddmm, '%d%m')
    
    # Format the date object as 'D Mon'
    formatted_date = date_obj.strftime('%-d %b')
    
    return formatted_date

def open_to_close(line, timedate):
    new_line = (line.replace('Open ', 'Close')[:52] + timedate + ' ' + line[66:]).replace('000000', '999999')
    return new_line

def parse_headers():
    header_line = 'MONEY      QTY         CAR        NZL PUMP   TRAN   TIME  DATE     FUEL       F.T  PAYMENT   CODE   ID                  ADD    WORKER  ODO      CHSPEC   RATE    DISCNT  DT   CT     CLUB                VOUCHER ST MS SNUM CUST_ID   AS CHECK_SUM NUM_CHECKS'
    # Find all header positions and lengths
    headers = header_line.split()

    # Find the starting indices of each header
    indices = []
    current_index = 0
    for header in headers:
        current_index = header_line.index(header, current_index)
        indices.append(current_index)

    return headers, indices

def parse_data(data_lines, indices):
    # Extract data based on header indices
    data = []
    for line in data_lines:
        row = [line[start:end].strip() for start, end in zip(indices, indices[1:] + [None])]
        data.append(row)
    return data

