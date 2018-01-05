
#		 Pair up the sentences
#		 For each word in the target sentence:
#		 	Compare to each word in the source sentence
#		 	Take the highest value, consider that word-pair a 'match'
#		 Take the average distance of all 'best word-pairs' in the sentences
#		 Compare this value for all sentence alignments
		 
		 
results = []
errors = 0		 
for t in range(0, len(lucan)): #take a target sentence
	target_sentence = lucan[t]
	sep_target = target_sentence.split()	
	for s in range(0, len(virgil)): # take a source sentence
		target_maxes = [] # this holds the best scores for each word in the target for this source pairing.
		source_sentence = virgil[s]
		sep_source = source_sentence.split()
		for tw in sep_target: # each target word one at a time 
			target_words_records = [] # reset the list of distances
			for sw in sep_source: # each source word one at a time
				try: # this is supposed to skip this word-pair if no vectors can be retrieved for either word
					dot = 1 - spatial.distance.cosine(vecs[tw], vecs[sw]) #the proximity between the word-pair
					target_words_records.append(dot)
				except KeyError:
					#print [tw, sw]
					pass 
			try:
				mx = max(target_words_records) # the highest proximity score for this target word. Will python do something stupid here?
			except ValueError:
				errors = errors + 1
				#print [lucan_names[t], lucan[t], v_names[s], virgil[s]]
			target_maxes.append(mx) # The last time this is called, it should have a number for each word in the target
		# This sentence pair is done, so take the average and create the record.
		av = sum(target_maxes) / float(len(target_maxes)) # will python do something stupid here?
		record = [lucan_names[t], lucan[t], v_names[s], virgil[s], av]
		results.append(record)
	

results.sort(key=itemgetter(4))

begin = len(results) - 20
end = len(results)

for i in range(begin,end):
		if results[i][4] != 'nan':
			print results[i]

