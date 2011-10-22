import re
wanted = [58, 56, 57, 51, 62, 55, 53, 60, 54, 66, 65, 63, 59, 61, 64, 52, 19, 21, 26, 25, 23, 
31, 22, 27, 45, 28, 33, 30, 32, 20, 18, 24, 34,
8, 11, 9, 48, 1, 16, 41, 42, 15, 6, 40, 46, 44, 12, 7, 47, 29, 13, 49, 14, 2, 4, 36, 0, 37, 5, 
3, 43, 38, 35, 17, 39, 50]

#for line in open('rod_control_input.pde'):
#	indexes = re.search(".*?ARDUBUS_DIGITAL_INPUTS { (.*) }", line)
#	if indexes:
#		indexes = indexes.group(1).split(', ')
#		for wi in wanted:
#			print indexes
#			print len(indexes)
#			print indexes[wi]

for index, pin in enumerate(wanted):
	signal = "control_rod_up"
	if index > len(wanted)/2:
		signal = "control_rod_down"
	print "%s%d=W, %d, %d" % (signal,index, pin, index) 


