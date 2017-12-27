from __future__ import division # it embarasses me that I need to import a module to do floating-point division.
import gensim
import numpy
from operator import itemgetter
from gensim.models.keyedvectors import KeyedVectors
from scipy import spatial
from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora, models, similarities
import re #having to import regular expression is even worse.
# there's probably a better way to handle this cltk importing than to do this every time, but for now...
import cltk
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from cltk.corpus.utils.importer import CorpusImporter
corpus_importer = CorpusImporter('latin')
corpus_importer.import_corpus('latin_models_cltk')
lemmatizer = LemmaReplacer('latin')
