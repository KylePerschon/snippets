# Author: Kyle Perschon
# Purpose: Mirror a tree of STL files into a new location, expanding any file
#          whose name encodes a quantity (e.g. "bracket_x4.stl") into that many
#          separately-named copies, so a slicer gets one file per physical part.
# %%
from glob import glob
from pathlib import Path
import shutil
import re

# --- Configure these two paths ---------------------------------------------
SOURCE_ROOT = r'C:\path\to\model\STL'
TARGET_ROOT = r'C:\path\to\model\STL expanded'
# ---------------------------------------------------------------------------

# Matches a trailing "x<digits>" just before the extension: bracket_x4.stl -> 4
QUANTITY_PATTERN = r"x(\d+)(?=\.[^.]+$|$)"

unique_files = 0
total_files = 0


def target_path_for(source_path) -> str:
    """Same relative location, under TARGET_ROOT instead of SOURCE_ROOT."""
    return str(source_path).replace(SOURCE_ROOT, TARGET_ROOT)


def copy_one_file(file_path):
    global total_files, unique_files
    shutil.copyfile(file_path, target_path_for(file_path))
    unique_files += 1
    total_files += 1


def copy_multiple_files(file_path, num_times):
    """Write num_times copies, each named "<n>_of_<total>" in place of "x<total>"."""
    global total_files, unique_files
    new_file_path = target_path_for(file_path)
    unique_files += 1
    for i in range(int(num_times)):
        new_appendix = f"{i + 1}_of_{num_times}"
        copy_to_this_file = new_file_path.replace(f'x{num_times}', new_appendix)
        shutil.copyfile(file_path, copy_to_this_file)
        total_files += 1


def make_new_directory(dir_path, parents=False):
    Path(target_path_for(dir_path)).mkdir(parents=parents, exist_ok=True)


def duplicate_files(path):
    for file in glob(f"{path}/*"):
        f = Path(file)

        if f.is_dir():
            # Create the mirror directory before descending, so children have a
            # parent to be written into.
            make_new_directory(file)
            duplicate_files(f)
            continue

        regex_match = re.search(QUANTITY_PATTERN, f.name)
        if regex_match:
            copy_multiple_files(file, regex_match.group(1))
        else:
            copy_one_file(file)


if __name__ == '__main__':
    if not Path(SOURCE_ROOT).is_dir():
        raise SystemExit(f'Source folder not found: {SOURCE_ROOT}')

    make_new_directory(SOURCE_ROOT, parents=True)
    duplicate_files(SOURCE_ROOT)

    print(f"{'-' * 5} Status report {'-' * 5}")
    print(f"Unique files: {unique_files}")
    print(f"Total files written: {total_files}")
# %%
