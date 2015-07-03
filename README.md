## A simple Python tool to do basic subtitle modifications

This is a standalone Python 3 script to modify .srt subtitle files by
* shifting subtitles to the front or back
* modifying subtitle speed

### Notes:
* If you shift subtitles before the beginning, they will wrap around to 23 hours 59 minutes and vice versa. The ordering will not be adjusted.
Therefore durations longer than 24 hours are not supported.
* Subtitles containing " --> " will cause a failure.
