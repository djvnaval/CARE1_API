def splitter(path, filename):
	arr = []
	fr = open(f"{path}{filename}", 'r')

	for line in fr:
		x = line.split()
		arr.append(x[1])

	fr.close()
	return arr


def remove_negative(path, larger, smaller):
	out = open(f"{path}pos_{f1}", 'w')
	out.close()

	out = open(f"{path}pos_{f1}", 'a')

	for i in range(len(larger)):
		if float(larger[i]) - float(smaller[i]) >= 0:
			write = str(float(larger[i]) - float(smaller[i])) + '\n'
			out.write(write)

	out.close()

#remove_negative("post process.txt")
f1 = "testipe_2023-06-29 03:37:32.txt" # smaller
f2 = "HTTPSmartFarm_solenoidValve_actuate_2023-06-29 03:36:45.txt" # larger
path = "data/log/"

remove_negative(path, splitter(path, f2), splitter(path, f1))