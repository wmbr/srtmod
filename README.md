## A simple Python tool to do basic subtitle modifications

This is a standalone Python 3 script to modify .srt subtitle files by
* shifting subtitles to the front or back
* modifying subtitle speed

```
Usage: srtmod.py <operation>
	operation: one of '+number', '-number', '*number' 
	           where the first two shift the subtitles the given amount of milliseconds to the back
	           and the third one slows them down by the given factor
Subtitles are read from stdin.
Examples:
	Move subs one second to the front: srtmod.py -1000 < subtitles.srt
	Speed up subs by 2%:               srtmod.py *0.98 < subtitles.srt
```

### Notes:
* If you shift subtitles before the beginning, they will wrap around to 23 hours 59 minutes and vice versa. The ordering will not be adjusted.
Therefore durations longer than 24 hours are not supported.
* Subtitles containing " --> " will cause a failure.
