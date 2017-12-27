#The point of this script is to load up a model, load a set of target documents, compare those against a set of source documents, get the similarity scores through simple vector averaging, and then build a table of the results.
from vortex import dependencies
from vortex import tfidfModels
from vortex import loadFiles
from vortex import averages

# train a set of vectors...
string = dependencies.gensim.models.word2vec.LineSentence('corpora/all_latin.phrase.txt')
model = dependencies.gensim.models.Word2Vec(string, size=200, window=5, min_count=5, workers=4)
vecs = model.wv

#create the tf-idf model
[dictionary, corpus] = tfidfModels.buildModel('corpora/all_latin.doc.txt', string)

#build the inverse document frequency
docFreq = tfidfModels.docGen('corpora/all_latin.doc.txt')

# read the target file
[lucan, lucan_names] = loadFiles.loadFile("short_test/lucan.tess", "short_test/lucan_loci.tess")
[virgil, v_names] = loadFiles.loadFile("short_test/virgil.tess", "short_test/virgil_loci.tess")

#declare some empty lists which will contain the sentence-summary vectors
lucan_vectors = []
virgil_vectors = []

#create term frequency dictionaries for each text
vTf = tfidfModels.termGen('corpora/virgil.oneline.txt')
lTf = tfidfModels.termGen('corpora/lucan_sample.oneline.txt')

# default number of vectors
v = [0] * 200

# create average vectors for every sentence
for s in lucan:
	lucan_vectors.append(averages.weightedAverage(s, lTf, 5)
	
for s in virgil:
	virgil_vectors.append(averages.weightedAverage(s, lTf, 5)

# the results object is a list of tuples 
results = []

for i in range(0, len(lucan_vectors)):
	for n in range(0, len(virgil_vectors)):
		dot = 1 - dependencies.spatial.distance.cosine(lucan_vectors[i], virgil_vectors[n])
		tup = (lucan_names[i], lucan[i], v_names[n], virgil[i], dot)
		results.append(tup)

# the length of the results list is the cartesian product of the number of lines in each 'test' file. Take only the top-n by dot product.

sorted_results = results.sort(key=itemgetter(4))

begin = len(results) - 50
end = len(results)

for i in range(begin,end):
		if results[i][2] != 'nan':
			print results[i]

