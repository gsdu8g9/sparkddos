#
#   Simple class to listen to 1usagov streams.
#   AXJ 2016
#

import urllib2
import time

print "Recording..."

response = urllib2.urlopen("http://developer.usa.gov/1usagov")
filename = time.strftime("%Y%m%d%H%M%S", time.localtime())+".json"
f = open(filename, 'wb')

fileSizeStart = 0
fileSizeEnd = 28*1048576
block_size = 1024

progress = fileSizeEnd/100
increment = fileSizeEnd/20

while True:
	try:
		buffer = response.read(block_size)
		if not buffer:
			break

		fileSizeStart += len(buffer)
		if fileSizeStart > fileSizeEnd:
			break
		
		f.write(buffer)

	except Exception, e:
		print e

f.close()
print "Done."