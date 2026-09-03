# STL Batch Organizer

Sorts a few hundred STL files into folders by print setting and filament color,
copying and renaming each one along the way.

## The problem

A large 3D-printed RC model ships as a flat directory of STL files named by part
number (`24L-1-A.stl`), while the build documentation lives in a spreadsheet that
says which print profile and which filament color each part needs. Printing it
means grouping every part that shares a profile and a color into one batch —
otherwise you're changing settings and swapping filament a hundred times.

Doing that by hand for 115 parts is an afternoon, and one misfiled part means a
reprint.

## How it works

Paste the spreadsheet straight from Google Sheets into `RAW_DATA` — no CSV export,
no cleanup. Sheets copies as tab-separated text, so `csv.DictReader` reads it
directly out of a `StringIO` with `delimiter='\t'`, and the header row names the
columns for you.

Each row is then copied from the source directory into
`TARGET_DIR/<print setting>/<color>/`, renamed to the spreadsheet's combined name
(which encodes quantity — `70_x44.stl` is the part you need 44 of). Target folders
are created on demand.

Missing source files are collected rather than raised, so one typo in the
spreadsheet doesn't abort a run that's already copied ninety files. The summary at
the end lists exactly what couldn't be found.

`shutil.copy2` preserves timestamps, and the originals are never touched — a bad
run is fixed by deleting the output folder.

## Usage

```bash
python dozer_to_folders.py
```

Set `SOURCE_DIR` and `TARGET_DIR` at the top, and replace `RAW_DATA` with your own
paste. Required columns: `Original STL File Name`, `Print Setting Suffix`,
`Combined New File Name`, `Color`.

Standard library only.

## Note

`RAW_DATA` here holds five sample rows showing the expected shape. The original ran
against a 115-row manifest for a 1/14 scale D11 dozer.
