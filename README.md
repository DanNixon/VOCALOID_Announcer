# VOCALOID Announcer

Tool for creating announcement sound files from VSQ files and an exported audio
track.

## To use

1. Create/load a VSQ and export a WAV
2. If creating a new VSQ, create a new source `.json` file
3. Create a new target `.json` if required
4. Install and run the converter (see `vocaloid_announcer_conv -h` for usage)
5. Use the sound files!

## VSQ file requirements

- The start of the audio file must align with the start of first part/region in
  the VSQ
- The entire file should be a constant tempo
- Ideally there should be either a quarter note or eighth note spacing between
  the start of a region and the first note and between the end of one region and
  the start of the next
