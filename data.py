
import csv

def load_data(filename, delimiter=';', mode='rb'):
	f = open(filename, mode)
	return csv.reader(f, delimiter=delimiter)

def parse_reader(reader):
	ln = 0
	data = []
	for row in reader:
		print('row',row)
		if ln == 0:
			keys = row
			ln += 1
		elif ln > 0:
			entry = {}
			for col in range(len(keys)):
				entry[keys[col]] = row[col]
				print('k,v',entry)
			data += [entry]
		print('data',data)
	return data

def read(filename, delimiter=';'):
	reader = load_data(filename)
	data = parse_reader(reader)
	return data

