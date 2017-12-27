def loadFile(filename, tagfile):
	file = open(filename, "r")
	text = file.readlines()
	text = [x.strip() for x in text]
	tags = open(tagfile, "r")
	tags = tags.readlines()
	tags = [x.strip() for x in tags]
	return [text, tags]
