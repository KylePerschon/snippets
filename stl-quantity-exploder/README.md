# STL Quantity Exploder

Mirrors a folder tree of STL files into a new location, turning any file whose name
encodes a quantity into that many individually-named copies.

`chassis_rail_x4.stl` becomes `chassis_rail_1_of_4.stl` through
`chassis_rail_4_of_4.stl`, in the same relative folder.

## The problem

Large 3D-printable models are distributed with the part count baked into the
filename — one `bracket_x6.stl` means print six. But a slicer works on files: to
print six you either import the same file six times and manually track which copies
you've placed, or you duplicate it by hand six times first.

Do that across a model with a couple of hundred parts and you lose an evening and
still end up printing five of something.

## How it works

Walks the source tree recursively, creating each mirror directory *before*
descending into it so children always have a parent to be written into. For each
file it looks for a trailing `x<digits>` immediately before the extension:

```python
QUANTITY_PATTERN = r"x(\d+)(?=\.[^.]+$|$)"
```

The lookahead is what makes this safe. `x` followed by digits appears inside plenty
of legitimate part names — `box40`, `axle_x2_mount` — and a looser pattern matches
those too. Requiring the match to sit immediately before the final extension (or the
end of the name) means only a genuine trailing quantity counts.

Files with no quantity marker are copied once. The originals are never modified —
everything is written to a separate root, so a bad run is fixed by deleting the
output folder.

Ends with a count of unique parts versus total files written, which is the number
worth sanity-checking before you start a print queue.

## Usage

Set `SOURCE_ROOT` and `TARGET_ROOT` at the top of the file, then:

```bash
python explode_files.py
```

Standard library only. Works with UNC paths (`\\host\share\...`) as well as local
ones.

## Related

[stl-batch-organizer](../stl-batch-organizer/) solves the next step — sorting the
resulting files into batches by print setting and filament colour.
