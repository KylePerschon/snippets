# RGB Picker

Opens a live webcam feed. Click any pixel and it prints that pixel's RGB value and
coordinates to the console.

## The problem

Computer vision work usually starts with a threshold or a color mask, and to write
one you need actual numbers — the real RGB of the thing you're detecting, under the
lighting you'll actually have. Guessing "that's roughly orange" and typing in a
range is how you end up tuning constants blind.

Sampling a saved screenshot in an image editor doesn't help either, because the
webcam's own color response and the room's lighting are part of what you're
measuring.

## How it works

An OpenCV mouse callback on the display window catches left clicks and indexes the
current frame at the click coordinates. OpenCV stores frames as BGR rather than
RGB, so the channels are pulled out by index and labelled explicitly instead of
trusting the tuple order — the single most common source of "my mask matches
nothing" in OpenCV.

Coordinates are printed alongside the color, which is what you need when you're
also working out where in the frame to look.

## Usage

```bash
pip install opencv-python numpy
python rgb_picker.py
```

Click anywhere in the window to sample. Press `Esc` to quit.

Uses capture device `0` — change it if you have more than one camera.
