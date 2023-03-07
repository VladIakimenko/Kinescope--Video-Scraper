def join_files(files, output_name):
	with open(output_name, 'wb') as output:
		for file in files:
			with open(file, 'rb') as video_file:
				output.write(video_file.read())


if __name__ == '__main__':
	file_list = [input('Enter file name (and path):\t') 
				 for _ in range(int(input('Number of files to be joined:\t').strip()))]
	name = input('Enter output name (and path):\t')
	
	join_files(file_list, name)
	input()
