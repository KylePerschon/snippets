# Servo Range Map

Bench-tests a throttle-byte to servo-angle mapping in plain Python, so the
arithmetic can be checked before it reaches hardware.

## The problem

A wireless throttle sends motor speed as a single byte, 0–255, plus a direction
flag. The motor driver expects a servo-style signal, 0–180, where the **midpoint**
means stop — above it is forward, below it is reverse. So one input range has to
fan out into two opposing output ranges that share an origin in the middle.

Getting that backwards means a locomotive that accelerates when you brake. That is
not a thing you want to discover by flashing the board and watching.

## How it works

`map_range` is the standard linear remap, integer-floored to match Arduino's
`map()` so the Python bench and the firmware agree. `get_speed` then sweeps the
full 0–255 input in both directions and prints each mapped result.

Reading the output top to bottom, an inverted axis or an off-by-one at the
endpoints is obvious — forward should climb from the midpoint to 180, reverse
should fall from the midpoint to 0, and both should hit exactly the midpoint at
input 0.

## Usage

```bash
python convert_test.py
```

No dependencies. Adjust `min_servo` / `max_servo` for a driver with a different
range.

Written as a `# %%` cell script.

## Related

Used while building [Locomotive-Controller](https://github.com/KylePerschon/Locomotive-Controller),
a wireless nRF24L01 throttle for a ride-on scale locomotive.
