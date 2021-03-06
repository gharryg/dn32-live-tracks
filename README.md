# DN32-LIVE Tracks

This is a sloppy tool created to extract mono tracks from many multichannel WAV files generated by the SD card recorder on the [DN32-LIVE](https://www.klarkteknik.com/Categories/Klarkteknik/Mixers/Accessories/DN32-LIVE/p/P0DN1) expansion module for Behringer and Midas audio consoles.

## Requirements

This was created and tested with Python 3.7 but should work with Python 3.3+. [ffmpeg](https://www.ffmpeg.org/) must be installed and in your path.

If you're on a Mac, it is available to install via Homebrew:
```
$ brew install ffmpeg
```

## How to Use

With this tool you can either specify a list of channels as an argument by using `--channels` or provide a file containing a list of channels by using `--files`.
```
$ cd dn32-live-tracks
$ python3 dn32-live-tracks.py --channels 1:Kick 2:Snare --files /path/to/multichannel/file1.wav /path/to/multichannel/file2.wav --output ~/Music/Tracks
```
**NOTE:** When specifying channel numbers, use the numbers as they are displayed on the console (not the channel numbers as they are in the WAV file).

## Why not just use a DAW?

It is true that most commonly used DAWs support importing multichannel WAV files; some DAWs even let you merge multiple tracks that are on the same channel (like the Glue Tool in Logic Pro X). My reasons for preferring this tool are:
 1. I often only need some of the 32 channels. No need to have the DAW split out channels that I don't need.
 2. It's nice to have all the tracks named before importing. In addition, it's easier to manage and archive media assets when they're clearly defined.
 3. I think this is faster in most cases.
