

print 'line intersects (1, 1), (9, 9)'

def isAboveLine(a, b, c):
		return ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])) > 0

for x in range(0,10,2):
	for y in range(0,10,2):
		c=(x, y)
		print str(c) + ' is above line? ' + str(isAboveLine((1,1), (9,9), c))
