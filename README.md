# Snippets

Small, self-contained utilities I've written over the years — each one solved a
real problem once and turned out to be worth keeping. Too small to be their own
repositories, too useful to lose in a Downloads folder.

Every snippet is a single file with no build step. Each folder has its own README
explaining the problem it solved and how to run it.

| Snippet | What it does | Language |
|---|---|---|
| [stl-batch-organizer](stl-batch-organizer/) | Sorts hundreds of 3D-print STL files into folders by print setting and filament color, driven by a pasted spreadsheet | Python |
| [serial-capture](serial-capture/) | Timestamps and buffers an Arduino serial stream so intermittent faults can be counted instead of guessed at | Python |
| [servo-range-map](servo-range-map/) | Bench-tests a throttle-byte → servo-angle mapping without flashing hardware | Python |
| [rgb-picker](rgb-picker/) | Click any pixel in a live webcam feed and print its RGB value and coordinates | Python |
| [nextjs-prisma-ops](nextjs-prisma-ops/) | Operations reference for running a Next.js + Prisma app on EC2 under PM2 | Reference |

## Why a single repo

These are utilities, not products. Keeping them together means one place to look,
one place to add the next one, and a single README that says what each is for —
rather than five near-empty repositories with one file each.
