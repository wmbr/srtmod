#!/usr/bin/env python3

from datetime import datetime, timedelta
from functools import partial
from operator import add, mul
import os
import sys
import textwrap

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

def process_line(line, op):
	start, end = line.split(" --> ", maxsplit=1)
	
	start = timedelta_parse(start)
	end = timedelta_parse(end)

	start = op(start)
	end = op(end)
	
	start = timedelta_format(start)
	end = timedelta_format(end)
	return start + " --> " + end
	
	
def process_file(file, op):
	result = []
	for line in file:
		line = line.strip()
		if line.find("-->") != -1:
			line = process_line(line, op)
			
		result.append(line)
	
	return "\n".join(result)


def print_help():
	print(textwrap.dedent(
	"""
	Usage: {program} <operation>
		operation: one of '+number', '-number', '*number' 
		           where the first two shift the subtitles the given amount of milliseconds to the back
		           and the third one slows them down by the given factor
	Subtitles are read from stdin.
	Examples:
		Move subs one second to the front: {program} -1000 < subtitles.srt
		Speed up subs by 2%:               {program} *0.98 < subtitles.srt
	""".format(program=os.path.basename(sys.argv[0]))))


def parse_operation(op_string):
	try:
		if len(op_string) >= 2:
			if op_string[0] in ['+', '-']:
				delta = timedelta(milliseconds=int(op_string))
				return partial(add, delta)
			elif op_string[0] == '*':
				factor = float(op_string[1:])
				return partial(mul, factor)
	except ValueError:
		pass
	raise ValueError("Invalid operation: '{}'".format(op_string))


def main():
	if len(sys.argv) == 2:
		try:
			op = parse_operation(sys.argv[1])
			sys.stdout.write(process_file(sys.stdin, op))
		except ValueError as v:
			print(v)
			print_help()
	else:
		print_help()


main()