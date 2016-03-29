# VOCALOID Announcer

Tool for creating announcment sound files from VSQ files and an exported audio
track.

The various messages are defines in several VSQ files and split by the
`converter` script using data in the JSON files to output a folder to be dropped
into the radios SD card.

## To use

1. Create/load a VSQ and export a WAV
2. If creating a new VSQ, create a new source `.json` file
3. Create a new target `.json` if required
4. Run the `converter` script (run `./converter -h` for usage)
5. Use the sound files!

## VSQ file requirements

- The start of the audio file must align with the start of first part/region in
  the VSQ
- The entire file should be a constant tempo
- Ideally there should be either a quarter note or eighth node spacing between
  the start of a region and the first node and between the end of one region and
  the start of the next

## Requirements

- [Pydub](https://github.com/jiaaro/pydub)
- [xmltodict](https://github.com/martinblech/xmltodict)
