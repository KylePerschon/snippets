# Author: Kyle Perschon
# Purpose: Recursively translate file and folder names from one language to
#          another, in place. Written for a German 3D-model kit whose several
#          hundred part names were unreadable.
# %%
from glob import glob
from pathlib import Path

from deep_translator import GoogleTranslator

# --- Configure ------------------------------------------------------------
TARGET_FOLDER = r'C:\path\to\folder'
SOURCE_LANG = 'de'
TARGET_LANG = 'en'

# Leave True until the printed renames look right. Nothing is touched while
# this is on — renaming a tree of filenames is not something you can undo.
DRY_RUN = True
# -------------------------------------------------------------------------

translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)


def translated_name(path: Path) -> str:
    """Translate the stem, keep the extension untouched.

    Translating the whole filename sends the extension to the API too, which
    happily turns ".stl" into something else. Splitting first means the suffix
    is preserved by construction rather than repaired afterwards.
    """
    stem, suffix = path.stem, path.suffix

    try:
        new_stem = translator.translate(stem)
    except Exception as e:
        print(f'  ! translation failed for {path.name!r}: {e}')
        return path.name

    if not new_stem:
        return path.name

    # Strip characters that are illegal in Windows filenames.
    for bad in '<>:"/\\|?*':
        new_stem = new_stem.replace(bad, '')
    new_stem = new_stem.strip().rstrip('.')

    if not new_stem:
        return path.name

    return f'{new_stem}{suffix}'


def translate_tree(folder: Path):
    # Collect first: renaming entries while globbing the same directory gives
    # inconsistent results.
    entries = [Path(p) for p in glob(f'{folder}/*')]

    for entry in entries:
        # Descend before renaming, so the recursion uses paths that still exist.
        if entry.is_dir():
            translate_tree(entry)

        new_name = translated_name(entry)
        if new_name == entry.name:
            continue

        destination = entry.with_name(new_name)
        if destination.exists():
            print(f'  skip (target exists): {entry.name} -> {new_name}')
            continue

        print(f'  {entry.name}  ->  {new_name}')
        if not DRY_RUN:
            entry.rename(destination)


if __name__ == '__main__':
    root = Path(TARGET_FOLDER)
    if not root.is_dir():
        raise SystemExit(f'Folder not found: {TARGET_FOLDER}')

    print(f'{"DRY RUN - nothing will change" if DRY_RUN else "RENAMING FILES"}')
    print(f'{SOURCE_LANG} -> {TARGET_LANG} in {root}\n')
    translate_tree(root)
    print('\nDone.' if not DRY_RUN else '\nDry run complete. Set DRY_RUN = False to apply.')
# %%
