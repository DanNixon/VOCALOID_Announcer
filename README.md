# OpenTX VOCALOID Voices

Voice packs for OpenTX created with VOCALOID.

The various messages are defines in several VSQ files and split by the
`converter` script using data in the JSON files to output a folder to be dropped
into the radios SD card.

## To use

1. Load the VSQs in to VOCALOID and export a WAV
2. Load the WAV into an editor such as Audacty
3. Convert it to mono by splitting the stereo track, removing one and setting
   the other to mono
4. Set the project sample rate to 32000 Hz
5. Export a new WAV to the `source` folder
6. Run the `converter` script
7. Upload to TX

Steps 2 - 5 may not be needed on some radios (e.g. Taranis) but definitely are
on radios such as the 9XR-PRO.

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
