import math

def read_data(fname):
	temp_data=[]
	try:
		with open(fname) as docs:
			for line in docs:
				line=map(float,line.split())
				temp_data.append(line)

	except Exception,e:
		raise e
		print "File Not Found, program will exit"
		exit()

	return temp_data

def read_labels_data(fname):
	temp_data=[]
	try:
		with open(fname) as docs:
			for line in docs:
				if "-" in line:
					temp_data.append(0)
				else:
					temp_data.append(1)

	except Exception,e:
		raise e
		print "File Not Found, program will exit"
		exit()

	return temp_data

def calculate_unique(labels):
	unique={}
	data_entropy=0.0
	for elem in labels:
		if elem in unique:
			unique[elem]=unique[elem]+1
		else:
			unique[elem]=1

	return unique


def calculate_gain(labels,tuples):
	labels=tuples["total"]
	del tuples["total"]
	entropy=calculate_entropy(labels,tuples)
	return entropy


def gain(data,single_attribute,column,dict_for_entropy):
	unique=calculate_unique(single_attribute)
	occurences={}
	for elem in data:
		if elem[column] in unique:
			if elem[column] in occurences:				
				if elem[-1] in occurences[elem[column]]:
					occurences[elem[column]][elem[-1]]=occurences[elem[column]][elem[-1]]+1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
				else:
					occurences[elem[column]][elem[-1]]=1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
			else:
				occurences[elem[column]]={elem[-1]:1}
				occurences[elem[column]]["total"]=1

	info_gain=0.0
	for keys in occurences:
		Dj=occurences[keys]["total"]
		D=len(data)
		info_gain=info_gain+(float(Dj)/D)*calculate_gain(len(single_attribute),occurences[keys])
	dict_for_entropy[info_gain]=column
	return info_gain,dict_for_entropy

def choose_best_attribute(data,list_of_attributes,class_labels,gain):
	unique=calculate_unique(class_labels)
	total_entropy=calculate_entropy(len(class_labels),unique)
	best_gain=0.0
	entropy_results={}
	
	for i in range(len(list_of_attributes[0])):
		label_by_label=[]
		for j in range(len(list_of_attributes)):
			label_by_label.append(list_of_attributes[j][i])
		
		info_gain,entropy_results=gain(data,label_by_label,i,total_entropy,entropy_results)
		if info_gain>best_gain:
			best_gain=info_gain
		else:
			continue

	return(entropy_results[best_gain])


def calculate_entropy(labels,unique):
	data_entropy=0.0
	for frequency in unique.values():
		data_entropy -= (float(frequency)/labels) * math.log(float(frequency)/labels, 2)


	return data_entropy 



def main(fname1,fname2):
	file_name=fname1	
	list_of_attributes=read_data(file_name)
	file_name=fname2
	class_labels=read_labels_data(file_name)
	column_attribute=[]
	for i in range(len(list_of_attributes[0])):
		temp=[]
		for j,row in enumerate(list_of_attributes):
			temp.append(row[i])
		column_attribute.append(temp)

	column_total_data=[]
	for temp in column_attribute:
		total=reduce(lambda x,y:x+y,temp)
		split=float(total)/len(temp)
		feature=[]
		for item in temp:
			if item<split:
				feature.append("X")
			else:
				feature.append("Y")
		column_total_data.append(feature)
		
	data=[[1 for i in range(len(column_total_data))] for j in range(len(column_total_data[0]))]
	for i in range(len(column_total_data)):
		for j in range(len(column_total_data[0])):
			data[j][i]=column_total_data[i][j]

	input_data=[]
	for item in data:
		input_data.append(''.join(item))

	return input_data

		

			
