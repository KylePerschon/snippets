# Author: Kyle Perschon
# Created: 2026-09-02
# Description: Organizes STL files by print setting and color based on a
#              pasted Google Sheets dump. Copies and renames source .stl files
#              into structured target folders (e.g., TARGET_DIR/P1/Y/).
# %%
import os
import shutil
import io
import csv

# 1. Paste your unformatted Google Sheets dump inside the triple quotes below
RAW_DATA = """Original STL File Name	Part Number	Print Setting Suffix	Combined New File Name	Quantity	Color
1-1-A	1	P2	1_x1	1	Y
3-1-A	3	P1	3_x1	1	Y
10-1-A	10	P2	10_x2	2	Y
31-1-A	31	P5	31_x1	1	B
70-44-A	70	P7	70_x44	44	B"""

# 2. Update these paths for your computer setup
SOURCE_DIR = r"C:\path\to\STL DATABASE"
TARGET_DIR = r"C:\path\to\Organized STL Files"


def organize_stl_files():
    # Use io.StringIO to let python's csv module read the raw text string directly
    csv_file = io.StringIO(RAW_DATA.strip())
    reader = csv.DictReader(csv_file, delimiter='\t')
    missing_files = []
    copied_count = 0

    for row in reader:
        print(row)
        # Pull key values from your spreadsheet columns
        orig_name = row['Original STL File Name'].strip()
        print_setting = row['Print Setting Suffix'].strip()
        new_name = row['Combined New File Name'].strip()
        color = row['Color'].strip()
        
        # Build out target paths: Output/P1/Y/ or Output/P4/B/
        dest_folder = os.path.join(TARGET_DIR, print_setting, color)
        
        # Ensure the filename has the standard .stl extension
        src_filename = f"{orig_name}.stl"
        dest_filename = f"{new_name}.stl"
        
        src_path = os.path.join(SOURCE_DIR, src_filename)
        dest_path = os.path.join(dest_folder, dest_filename)
        
        # Check if file exists in source folder before running operations
        if os.path.exists(src_path):
            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            copied_count += 1
            print(f"Copied & Renamed: {src_filename} -> {print_setting}/{color}/{dest_filename}")
        else:
            missing_files.append(src_filename)

    # Summary reporting
    print("\n" + "=" * 40)
    print(f"Task complete! Successfully processed {copied_count} files.")
    if missing_files:
        print(f"⚠️ Could not find {len(missing_files)} files in source directory:")
        for f in missing_files:
            print(f"  - {f}")
    print("="*40)

if __name__ == "__main__":
    organize_stl_files()
# %%
