from .info_extract import stanfordDir, parserModelsPath, modelPath

import os
import os.path

import nltk
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
from nltk.parse import stanford
from nltk.tokenize import word_tokenize
from nltk.tree import Tree
from nltk.draw.tree import TreeView
from nltk.tokenize import sent_tokenize

# NER
nerClassifierPath = os.path.join(stanfordDir, 'ner', 'classifiers', 'english.all.3class.distsim.crf.ser.gz')

nerJarPath = os.path.join(stanfordDir, 'ner', 'stanford-ner.jar')

nerTagger = StanfordNERTagger(nerClassifierPath, nerJarPath)


# Postagger
postClassifierPath = os.path.join(stanfordDir, 'postagger', 'models', 'english-bidirectional-distsim.tagger')

postJarPath = os.path.join(stanfordDir, 'postagger', 'stanford-postagger.jar')

postTagger = StanfordPOSTagger(postClassifierPath, postJarPath)


# Parser

parserJarPath = os.path.join(stanfordDir, 'parser', 'stanford-parser.jar')

parser = stanford.StanfordParser(parserJarPath, parserModelsPath, modelPath)

depParser = stanford.StanfordDependencyParser(parserJarPath, parserModelsPath)

# Core
def openIE(target):
    if isinstance(target, list):
        target = '\n'.join(target)
    #setup the java targets
    coreDir = os.path.join()

    jarPath = os.path.join(stanfordDir, core, 'stanford-corenlp-3.8.0.jar')

    cp = '{}:CoreNLP-to-HTML.xsl:slf4j-api.jar:slf4j-simple.jar'.format(jarPath)
    with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as f:
        #Core nlp requires a files, so we will make a temp one to pass to it
        #This file should be deleted by the OS soon after it has been used
        f.write(target)
        f.seek(0)
        print("Starting OpenIE run")
        #If you know what these options do then you should mess with them on your own machine and not the shared server
        sp = subprocess.run(['java', '-mx2g', '-cp', cp, 'edu.stanford.nlp.naturalli.OpenIE', '-threads', '1', f.name], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        #Live stderr is non-trivial so this is the best we can do
        print(sp.stderr.decode('utf-8'))
        retSting = sp.stdout.decode('utf-8')
    #Making the DataFrame, again having to pass a fake file, yay POSIX I guess
    with io.StringIO(retSting) as f:
        df = pandas.read_csv(f, delimiter = '\t', names =['certainty', 'subject', 'verb', 'object'])
    return df
