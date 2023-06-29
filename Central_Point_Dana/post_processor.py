def splitter(path, filename):
	arr_large = []
	arr_small = []
	fr = open(f"{path}{filename}", 'r')

	for line in fr:
		x = line.split()
		arr_small.append(x[0])
		arr_large.append(x[1])

	fr.close()

	out = open(f"{path}pos_{filename}", 'w')
	out.close()

	out = open(f"{path}pos_{filename}", 'a')

	for i in range(len(arr_large)):
		if float(arr_large[i]) - float(arr_small[i]) >= 0:
			write = str(float(arr_large[i]) - float(arr_small[i])) + '\n'
			out.write(write)

	out.close()

#remove_negative("post process.txt")
f1 = "testipe_2023-06-29 03:37:32.txt" # smaller larger
path = "data/log/"

splitter(path, f1)