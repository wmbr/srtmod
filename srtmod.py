#!/usr/bin/env python3

from datetime import datetime, timedelta
from functools import partial
from operator import add, mul
import os
import sys
import textwrap

SEPARATOR = " --> "

class Operation:
	def __init__(self, opstring1, opstring2):
		delta1, time1 = self.parse_opstring(opstring1)
		delta2, time2 = self.parse_opstring(opstring2)
		if time1 == time2:
			self.ddelta = 0
		else:
			self.ddelta = (delta2 - delta1)/(time2-time1)
		self.delta0 = delta1 - self.ddelta*time1

	@staticmethod
	def parse_opstring(opstring):
		try:
			delta, _, time = opstring.partition("@")
			if delta == "":
				delta = "0"
			delta = timedelta(milliseconds=int(delta))
			if time == "":
				time = "0"
			time = timedelta_parse(time)
			return (delta,time)
		except ValueError:
			pass
		raise ValueError("Invalid operation: '{}'".format(opstring))

	def __call__(self, time):
		return time + self.delta0 + self.ddelta*time


def timedelta_parse(delta):
	hours = 0
	minutes = 0
	seconds = 0
	milliseconds = 0
	parts = delta.split(":")
	subminutes = parts[-1]
	if len(parts) >= 2:
		minutes = parts[-2]
		if len(parts) >= 3:
			hours = parts[-3]
	parts = subminutes.split(",")
	seconds = parts[0]
	if len(parts) >= 2:
		milliseconds = parts[1]
	return timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds), milliseconds = int(milliseconds))

def timedelta_format(delta):
	hours = delta.seconds // 3600
	minutes = delta.seconds // 60 % 60
	seconds = delta.seconds % 60
	milliseconds = delta.microseconds // 1000
	return "{:02}:{:02}:{:02},{:03}".format(hours, minutes, seconds, milliseconds)

def process_line(line, op):
	start, end = line.split(SEPARATOR, maxsplit=1)
	
	start = timedelta_parse(start)
	end = timedelta_parse(end)

	start = op(start)
	end = op(end)
	
	start = timedelta_format(start)
	end = timedelta_format(end)
	return start + SEPARATOR + end
	
	
def process_file(file, op):
	result = []
	for line in file:
		line = line.strip()
		if line.find(SEPARATOR) != -1:
			line = process_line(line, op)
			
		result.append(line)
	
	return "\n".join(result)


def print_help():
	print(textwrap.dedent(
	"""
	Usage: {program} [<delta>][@<time>] [<delta>][@<time>]
		delta:  One of '+number', '-number' where number is the amount of milliseconds to move the subtitles to the back. If omitted, "+0" is assumed.
		time:   Timestamp in format hh:mm:ss to denote the point at which the denoted shift is desired.
		        If omitted, "00:00:00" is assumed.

	By giving two operations with different times, subtitles may be slowed down or sped up.
	Subtitles are read from stdin.
	Examples:
		Move subs one second to the front everywhere: {program} -1000 < subtitles.srt
		Move subs 500ms to the front at 10min but keep the timing at 5min (speeding them up in result): {program} @5:00 -500@10:00 < subtitles.srt
	""".format(program=os.path.basename(sys.argv[0]))))


def main():
	args = sys.argv[1:]
	if len(args) == 1:
		args.append(args[0])
	if len(args) == 2:
		try:
			op = Operation(args[0], args[1])
			sys.stdout.write(process_file(sys.stdin, op))
		except ValueError as v:
			print(v)
			print_help()
	else:
		print_help()


main()
