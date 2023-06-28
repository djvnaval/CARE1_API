def splitter(filename):
	f1 = open(f"datetime_{filename}", 'w')
	f2 = open(f"seconds_{filename}", 'w')
	f1.close()
	f2.close()


	fr = open(filename, 'r')
	f1w = open(f"datetime_{filename}", 'a')
	f2w = open(f"seconds_{filename}", 'a')


	for line in fr:
		x = line.split()
		write1 = x[0] + '\n'
		write2 = x[1] + '\n'
		f1w.write(write1)
		f2w.write(write2)


	f1w.close()
	f2w.close()
	fr.close()

def remove_negative(larger, smaller):
	out = open(f"pos_{smaller}", 'w')
	out.close()

	large = open(larger, 'r')
	small = open(smaller, 'r')
	out = open(f"pos_{smaller}", 'a')
	largee = []
	smalll = []

	for line in large:
		largee.append(float(line))

	for line in small:
		smalll.append(float(line))

	for i in range(len(largee)):
		if largee[i] - smalll[i] >= 0:
			write = str(largee[i] - smalll[i]) + '\n'
			out.write(write)

	large.close()
	small.close()
	out.close()



#remove_negative("post process.txt")
f1 = "testipe_2023-06-27 12:22:14.txt" # smaller
f2 = "HTTPSmartFarm_solenoidValve_actuate_2023-06-27 12:21:56.txt" # larger

splitter(f1)
splitter(f2)
remove_negative(f"seconds_{f2}", f"seconds_{f1}")