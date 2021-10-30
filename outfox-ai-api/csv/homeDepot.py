with open('raw_data-unformated.csv') as f:
	lines = f.readlines()
	with open("raw_data.csv", "w") as text_file:
		for line in lines:
    			text_file.write(line.upper())
