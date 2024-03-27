def sort_file_by_values(file_path, from_line, to_line, from_int, to_int):
    with open(file_path, "r", encoding="utf-8-sig", errors='ignore') as file:
        lines = file.readlines()[from_line-1:to_line]

    # Extract integers from positions specified by from_int to to_int and convert it to integer
    values = [int(line[from_int-1:to_int]) for line in lines]

    # Zip lines and their corresponding values together, sort by the values, then unzip
    lines, _ = zip(*sorted(zip(lines, values), key=lambda x: x[1]))

    # Write the sorted lines back to the file
    with open(file_path, "w", encoding='utf-8-sig', errors='ignore') as file:
        file.writelines(lines)
    print("Done sorting the file")
# Usage
sort_file_by_values("/Users/talshaubi/Documents/GitHub/ROSEMAN/RS300124.D1A", 34, 322, 45, 52)
