def remove_consecutive_duplicates(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    filename_out = filename.split('.')[0] + '_no_duplicates.txt'  # output file
    
    with open(filename_out, 'w') as file_out:
        last_line = None
        for line in lines:
            if line != last_line:
                file_out.write(line)
            last_line = line

# Call the function with the file name
remove_consecutive_duplicates('/Users/talshaubi/Documents/GitHub/ROSEMAN/RS300124.D1A Scripted and half through.D1A')
