# OpenTX VOCALOID Voices

Voice packs for OpenTX created with VOCALOID.

The various messages are defines in several VSQ files and split by the
`converter` script using data in the JSON files to output a folder to be dropped
into the radios SD card.

## To use

1. Load the VSQs in to VOCALOID and export a WAV
2. Run the `converter` script
3. Upload to TX

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
