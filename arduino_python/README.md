# Arduino Python Tools

Two small Python utilities for bench-testing Arduino projects over serial —
written while debugging the radio link on
[Locomotive-Controller](https://github.com/KylePerschon/Locomotive-Controller).

## `read_arduino.py`

Captures a serial stream from an Arduino, timestamps every line as it arrives, and
buffers it for analysis. Written to answer one question: *how often is the radio
link actually dropping packets?*

The Arduino prints `failed to send` when a radio write isn't acknowledged. This
script tags each line with a `datetime` at the moment of receipt, collects up to
5,000 lines, then filters out the failures — turning "it seems flaky sometimes"
into a timestamped list you can count and correlate against distance, orientation
or interference.

Reads are wrapped so a malformed or partial line can't kill a capture mid-run.

```bash
pip install pyserial
python read_arduino.py
```

Port and baud rate are set in the call at the bottom of the file (`com3`, 9600).

## `convert_test.py`

A pure-Python bench for the throttle-to-servo mapping, so the arithmetic can be
verified without flashing a board.

The controller sends motor speed as a byte (0–255) plus a direction; the motor
driver expects a servo-style signal (0–180) where the *midpoint* is stop, values
above it are forward and values below are reverse. This script sweeps the full
input range in both directions and prints the mapped output, which makes an
off-by-one or an inverted axis obvious in a way that watching a locomotive lurch
does not.

```bash
python convert_test.py
```

No dependencies.

## Note

Both files are written as `# %%` cell scripts, meant to be stepped through
interactively in VS Code or Spyder rather than run start to finish.
