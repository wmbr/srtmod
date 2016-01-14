## A simple Python tool to do basic subtitle modifications

This is a standalone Python 3 script to modify .srt subtitle files by
* shifting subtitles to the front or back
* modifying subtitle speed

```
Usage: srtmod.py [<delta>][@<time>] [<delta>][@<time>]
	delta:  One of '+number', '-number' where number is the amount of milliseconds to move the subtitles to the back. If omitted, "+0" is assumed.
	time:   Timestamp in format hh:mm:ss to denote the point at which the denoted shift is desired.
	        If omitted, "00:00:00" is assumed.

By giving two operations with different times, subtitles may be slowed down or sped up.
Subtitles are read from stdin.
Examples:
	Move subs one second to the front everywhere: srtmod.py -1000 < subtitles.srt
	Move subs 500ms to the front at 10min but keep the timing at 5min (speeding them up in result): srtmod.py @5:00 -500@10:00 < subtitles.srt
```

### Notes:
* If you shift subtitles before the beginning, they will wrap around to 23 hours 59 minutes and vice versa. The ordering will not be adjusted.
Therefore durations longer than 24 hours are not supported.
* Subtitles containing " --> " will cause a failure.
