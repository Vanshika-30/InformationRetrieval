import os
import random

if __name__=='__main__':
	no_of_queries_per_document = 6

	outFile = open("inp.txt", 'w')

	dirname = os.getcwd()
	dirname = os.path.join(dirname,'Corpus/PreppedDocs')
	for filename in os.listdir(dirname):
		filepath = os.path.join(dirname,filename)
		lenths = [2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,6,6,7,8,8,9,9,10]
		with open(filepath,'r') as f:
			content = f.read()
			words = content.split(" ")
			for _ in range(100):
				start = random.randint(0,len(words))
				length = random.choice(lenths)
				# length = 2
				end = start + length

				query = " ".join(words[start:end])
				outFile.write(query)
				outFile.write('\n')