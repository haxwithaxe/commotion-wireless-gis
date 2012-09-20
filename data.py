

def load_data(filename, mode='r'):
	file_obj = open(filename, mode)
	file_string = file_obj.read()
	file_obj.close()
	return file_string

def parse_string(data_string, delimiter):
	ln = 0
	data = []
	for line in data_string.strip().split('\n'):
		print(line)
		line = line.replace('\r', '').strip()
		if line.startswith('#'): line = ''
		arr = line.split(delimiter)
		if ln == 0 and len(arr) > 1:
			keys = []
			for i in arr:
				keys += i.strip()
			ln += 1
		elif ln > 0:
			entry = {}
			for i in range(len(keys)):
				if i < len(arr): entry[keys[i]] = arr[i]
				else: entry[keys[i]] = None
			data += entry
		print('data',data)
	return data

def read(filename, delimiter=';'):
	data_string = load_data(filename)
	data = parse_string(data_string, delimiter)
	return data

