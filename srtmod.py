from datetime import datetime, timedelta
import os
import sys

def timedelta_parse(delta):
	hours, minutes, rest = delta.split(":")
	seconds, milliseconds = rest.split(",")
	return timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds), milliseconds = int(milliseconds))

def timedelta_format(delta):
	hours = delta.seconds // 3600
	minutes = delta.seconds // 60 % 60
	seconds = delta.seconds % 60
	milliseconds = delta.microseconds // 1000
	return "{:02}:{:02}:{:02},{:03}".format(hours, minutes, seconds, milliseconds)

def process_line(line, delta):
	start, end = line.split(" --> ", maxsplit=1)
	
	delta = timedelta(milliseconds = delta)
	
	start = timedelta_parse(start)
	end = timedelta_parse(end)

	start = start + delta
	end = end + delta
	
	start = timedelta_format(start)
	end = timedelta_format(end)
	return start + " --> " + end
	
	
def process_file(file, delta):
	result = []
	for line in file:
		line = line.strip()
		if line.find("-->") != -1:
			line = process_line(line, delta)
			
		result.append(line)
	
	return "\n".join(result)


def print_help():
	print("Usage: {program} DELTA\n\tDELTA: milliseconds to delay subitles \nExample: {program} -1000 < subtitles.srt".format(program=os.path.basename(sys.argv[0])))

def main():
	if len(sys.argv) == 2:
		try:
			delta = int(sys.argv[1])
			sys.stdout.write(process_file(sys.stdin, delta))
		except ValueError as v:
			print("ERROR:", v)
			print_help()
	else:
		print_help()


main()