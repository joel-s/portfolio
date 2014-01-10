#! /usr/bin/env python

import os
import sys
import re
import time

whereami="whereami"
user=os.environ["USER"]

def main(argv):
	searchString = user
	if len(argv) > 1:
		searchString = argv[1]

	ins, outs = os.popen4("%s %s" % (whereami, searchString))

	output = outs.readlines()

	times = parseWhereamiOutput(output)

	for k in times.keys():
		for entry in times[k]:
			starth = entry[0][3]
			startm = entry[0][4]
			if starth > 12:
				starth -= 12
				start = "%d:%.2dpm" % (starth, startm)
			elif starth == 12:
				start = "%d:%.2dpm" % (starth, startm)
			else:
				if starth == 0:
					starth = 12
				start = "%d:%.2dam" % (starth, startm)
				
			endh = entry[1][3]
			endm = entry[1][4]
			if endh > 12:
				endh -= 12
				end = "%d:%.2dpm" % (endh, endm)
			elif endh == 12:
				end = "%d:%.2dpm" % (endh, endm)
			else:
				if endh == 0:
					endh = 12
				end = "%d:%.2dam" % (endh, endm)

			insertAppt("%s@dayrunner" % user, entry[0], start, end, "\"%s machine time\"" % k)

def reprOfDate(date):
	return time.strftime("%m/%d/%y", date)

def insertAppt(cal, date, start, end, text):
	cmd = ("dtcm_insert -c " +cal
				 +" -d " +reprOfDate(date)
				 +" -s " +start +" -e " +end +" -w " +text)
	print "+", cmd
	return os.system(cmd +">/dev/null")

def parseWhereamiOutput(output):
	times = {}

	i = 0
	try:
		while i < len(output):
			if output[i].find("=") == -1:
				mo = re.search("Time assigned on (?P<machine>.*):", output[i])
				machine = mo.group("machine")
				times[machine] = []

				if output[i+1].find("=") != -1:
					i+=1
					continue

				while 1:
					i+=1
					mo = re.search("Appointments for (?P<date>.*):", output[i])
					date = mo.group("date")

					i+=1
					while 1:
						mo = re.search(".*[0-9]\) +(?P<starttime>[^-]*)-(?P<endtime>.[^ ]*) .*", output[i])
						starttime = "%s %s" % (mo.group("starttime"), date)
						endtime = "%s %s" % (mo.group("endtime"), date)
						start_t = time.strptime(starttime, "%I:%M%p %A %B %d, %Y")
						end_t = time.strptime(endtime, "%I:%M%p %A %B %d, %Y")

						times[machine].append((start_t, end_t))

						if output[i+1].find("Appointments") != -1:
							break
						if output[i+1].find("=") != -1:
							break

						i+=1

					if output[i+1].find("=") != -1:
						break

			i+=1
	except IndexError:
		pass

	return times


if __name__ == "__main__":
	sys.exit(main(sys.argv))
