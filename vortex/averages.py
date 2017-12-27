# determine the mean of all the vector representations that comprise a sentence

def sentenceAverage (text):
	separated = text.split()	
	fullvector = numpy.array(v, dtype='f') # this needs to be the length of all vectors
	successes = 0
	for w in separated:
		try:
			vecs[w]
			fullvector = fullvector + vecs[w]
			successes = successes + 1
		except KeyError:
			pass
	fullvector = fullvector / successes
	return(fullvector)
#Usage: 
#for s in virgil:
#	virgil_vectors.append(sentenceAverage(s))

def weightedAverage (text, termDict, terms): # needs a term frequency object created by tfidfModels.termGen() and how many words to pull out
	separated = text.split()	
	fullvector = numpy.array(v, dtype='f') # this needs to be the length of all vectors
	successes = 0
	if len(separated) > terms - 1:
		separated = tfidfModels.altTfWords(separated, termDict, terms)
	for w in separated:
		try:
			vecs[w]
			fullvector = fullvector + vecs[w]
			successes = successes + 1
		except KeyError:
			pass
	fullvector = fullvector / successes
	return(fullvector)



