f = open('wavelengths.txt', 'r')
wavelengths = []
for line in f:
	wavelengths.append(float(line.strip().split("\t")[0]))

print wavelengths
f.close()
