# Serial Capture

Reads an Arduino serial stream, timestamps every line at the moment it arrives,
and buffers it for analysis.

## The problem

Debugging a 2.4 GHz radio link between two Arduinos, the failure mode was "it seems
to drop packets sometimes." The board prints `failed to send` when a radio write
isn't acknowledged, but watching that scroll past in the Arduino IDE's serial
monitor tells you nothing you can act on — you can't count it, and you can't
correlate it with distance or antenna orientation.

## How it works

Each line gets a `datetime` stamp on receipt rather than on the Arduino side, which
keeps the microcontroller's loop free of string formatting and clock handling. The
capture runs to a fixed line limit so a session ends on its own instead of filling
memory, then the failures are filtered out into a countable list.

Reads are wrapped so a malformed or partially-received line yields `None` and the
loop continues — a garbled byte mid-capture doesn't cost you the run.

The output is a timestamped list you can count, diff between runs, and line up
against whatever you changed.

## Usage

```bash
pip install pyserial
python read_arduino.py
```

Port and baud are set in the call at the bottom (`com3`, 9600). Adjust
`limit_output_capture` for longer sessions.

Written as a `# %%` cell script for stepping through in VS Code or Spyder.
