# OpenTX VOCALOID Voices

Voice packs for OpenTX created with VOCALOID.

The various messages are defines in several VSQ files and split by the
`converter.py` script using data in the JSON files to determine the start and
end of each message.

## To use

1. Load the VSQs in to VOCALOID and export a WAV, ensure that measure 0 is at
   the start of the WAV
2. Load the WAV into an editor such as Audacty
3. Convert it to mono by splitting the stereo track, removing one and setting
   the other to mono
4. Set the project sample rate to 32000 Hz
5. Export a new WAV to the `source` folder
6. Run the `converter` script
7. Upload to TX

Steps 2 - 5 may not be needed on some radios (e.g. Taranis) but definitely are
on radios such as the 9XR-PRO.
