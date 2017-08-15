temp=[]
with open("west_soc_drop.txt") as f:
	for line in f:
		temp.append([float(x) for x in line.split()])
sum = 0
for i in xrange(1786):
	sum += temp[i][0]

print sum