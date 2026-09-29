# Translate Filenames

Recursively translates file and folder names from one language to another, in place.

Written after buying a German 3D-printable model kit whose several hundred part
files were named in German — unusable when you're trying to find the part the
instructions just referred to.

## How it works

Walks the tree, translating each name through `deep_translator`, and renames.

Three details do the real work:

**The extension is split off before translating.** This is the whole point. Sending
`Halterung.stl` to a translation API gets you a translated *extension* too, and the
file stops being an STL. Translating `path.stem` and reattaching `path.suffix` means
the suffix is preserved by construction rather than repaired afterwards with
string-matching that can get the boundary wrong.

**Recursion happens before renaming.** A folder is descended into first, then
renamed — otherwise the recursive call receives a path that no longer exists.

**Directory entries are collected before any renaming starts.** Renaming while
iterating the same directory gives inconsistent results depending on the filesystem.

Then the defensive bits: translated text is stripped of characters Windows won't
accept in a filename (`< > : " / \ | ? *`) and of trailing dots and spaces; a failed
API call or an empty translation leaves the original name alone rather than
producing something broken; and a rename that would collide with an existing file
is skipped and reported.

## Dry run first

`DRY_RUN = True` is the default. It prints every rename it *would* make and touches
nothing.

Renaming a few hundred files in place is not undoable, and machine translation of
short fragments out of context is unpredictable — a part name can come back as
something worse than the German. Read the list, then set `DRY_RUN = False`.

## Usage

```bash
pip install deep-translator
python translate_filenames.py
```

Set `TARGET_FOLDER`, `SOURCE_LANG` and `TARGET_LANG` at the top. Language codes are
the standard two-letter ones — `de`, `en`, `fr`, `ja`.

Translation goes through a free public endpoint, so a few hundred files is fine and
a few thousand may get rate-limited.
