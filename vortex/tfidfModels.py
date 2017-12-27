# takes the location of a newline-delimited corpus of all Latin, e.g. 'corpora/all_latin.doc.txt' and a LineSentence dependencies.gensim object
def buildModel(tfcorpus, string):
	docs = dependencies.gensim.models.word2vec.LineSentence(tfcorpus)
	dictionary = corpora.Dictionary(string)
	corpus = [dictionary.doc2bow(text) for text in docs]
	tfidf = models.TfidfModel(corpus)
	return [dictionary, corpus]


# build the term frequencies for a document
def termGen(filename):
	file = open(filename)
	content = file.readlines()	
	termfreq = []
	for wordstring in content:
		wordlist = wordstring.split()
		for w in wordlist:
		    termfreq.append(wordlist.count(w)/len(wordlist))
	termDict = dict(zip(wordlist, termfreq))
	return termDict

# takes the location of a newline-delimited corpus of all Latin, e.g. 'corpora/all_latin.doc.txt'
def docGen(corp):
	#docFreq is built as the map of uniquewords:documents_in_which_uniqueword_appears
	docFreq = dict()
	#grab each document as a string
	f = open(corp)
	content = f.readlines()	
	for wordstring in content:
		wordlist = wordstring.split()
		wordset = set(wordlist)
		for w in wordset:
			docFreq[w] = docFreq.get(w, 0) + 1
	for w in docFreq:
		docFreq[w] = dependencies.math.log(len(content) / docFreq[w]) # docFreq is replaced with the inverse doc frequency of each word
	return(docFreq)


#take a vector and return a vector containing only the highest tf-idf weighted words
#this method uses the default dependencies.gensim tfidf system, where 'term frequency' is defined by the input vector (sentence)
#pass in the objects created by buildModel as well as the phrase in question
def getTfWords (phrase, dictionary, corpus):
	vecmodel = [dictionary.doc2bow(phrase)]
	tfidfscores = tfidf[vecmodel[0]]
	#now figure out which ones to keep
	#one option: just take the top five words
	#requires error handling: what if the sentence has fewer than five words?
	tfidfscores.sort(key=itemgetter(1))
	start = len(tfidfscores) - 5
	stop = len(tfidfscores)
	sliceObj = slice (start,stop)
	substring = tfidfscores[sliceObj]
	#print substring
	#translate back into a vector of strings
	retstring = [None]*5
	for i in range(0,5):
	    number = substring[i][0]
	    word = dictionary[number]
	    plain = word.encode('ascii','ignore')
	    retstring[i] = plain
	return retstring


# this alternative tfidf score generator uses the full target or source text as the term frequency source, 
# and the full Latin corpus as doc frequency source 
#supports variable number of terms to extract
def altTfWords (phrase, termDict, terms):
	idfScores = []
	for w in phrase:
		termFreq = termDict[w]
		idf = docFreq[w]
		score = termFreq * idf
		idfScores.append(score)
	tfidfscores = zip(phrase,idfScores)
	tfidfscores.sort(key=itemgetter(1))
	start = len(tfidfscores) - terms
	stop = len(tfidfscores)
	sliceObj = slice (start,stop)
	substring = tfidfscores[sliceObj]
	#print substring
	#translate back into a vector of strings
	retstring = [None]*terms
	for i in range(0,terms):
	    word = substring[i][0]
	    retstring[i] = word
	return retstring
