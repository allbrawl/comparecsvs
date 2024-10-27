import os
import csv

def get_all_csv_files(root_folder):
    """
    Recursively find all CSV files in the folder and return a dictionary
    mapping the relative path of the file to its full path.
    """
    csv_files = {}
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith('.csv'):
                relative_path = os.path.relpath(os.path.join(dirpath, file), root_folder)
                csv_files[relative_path] = os.path.join(dirpath, file)
    return csv_files


def compare_csv_columns(file1, file2):
    """
    Compare columns of two CSV files and print the added or removed columns 
    using the csv module. Also prints the first row value of any added columns.
    """
    try:
        with open(file1, 'r', newline='') as f1, open(file2, 'r', newline='') as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)
            header1 = next(reader1)
            header2 = next(reader2)
            
            first_row_file2 = next(reader2, None)  

    except Exception as e:
        print(f"Error reading {file1} or {file2}: {e}")
        return

    columns1 = set(header1)
    columns2 = set(header2)

    added_columns = columns2 - columns1
    removed_columns = columns1 - columns2

    if added_columns:
        print(f"Added columns in {file2}:")
        for col in added_columns:
            try:
                col_index = header2.index(col)
                data_type = first_row_file2[col_index] if first_row_file2 else "N/A" 
                print(f"  - {col} (Type: {data_type})")
            except (ValueError, IndexError):
                print(f"  - {col} (Type: N/A)")

    if removed_columns:
        print(f"Removed columns in {file1}: {', '.join(removed_columns)}")


def compare_folders(folder1, folder2):
    """
    Compare CSV files from two folders and their subfolders.
    """
    files1 = get_all_csv_files(folder1)
    files2 = get_all_csv_files(folder2)

    for relative_path, file1 in files1.items():
        if relative_path in files2:
            file2 = files2[relative_path]
            print(f"Comparing {file1} and {file2}:")
            compare_csv_columns(file1, file2)
            print("-" * 50)

if __name__ == "__main__":
    folder1 = "base_csvs_v26"
    folder2 = "base_csvs"

    compare_folders(folder1, folder2)
