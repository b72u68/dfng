import os
import sys
from indexer import Indexer

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import INDEXFILE

if not os.path.isfile(INDEXFILE):
    print("[test] create index file: failed")
    print("unable to find index file.")
    exit(1)

try:
    indexer = Indexer().load_index()
except Exception as e:
    print("[test] load index: failed")
    print(e)
    exit(1)

test_document = """
BNF is a notation for Chomsky's context-free grammars. Backus was familiar with
Chomsky's work.[9]

As proposed by Backus, the formula defined "classes" whose names are enclosed
in angle brackets. For example, <ab>. Each of these names denotes a class of
basic symbols.[1]

Further development of ALGOL led to ALGOL 60. In the committee's 1963 report,
Peter Naur called Backus's notation Backus normal form. Donald Knuth argued
that BNF should rather be read as Backus-Naur form, as it is "not a normal form
in the conventional sense",[10] unlike, for instance, Chomsky normal form. The
name Pāṇini Backus form was also once suggested in view of the fact that the
expansion Backus normal form may not be accurate, and that Pāṇini had
independently developed a similar notation earlier.[11]
"""

test_result = ['bnf', 'notation', 'chomsky', 'context', 'free', 'grammars',
               'backus', 'familiar', 'chomsky', 'work', 'proposed', 'backus',
               'formula', 'defined', 'classes', 'whose', 'names', 'enclosed',
               'angle', 'brackets', 'example', 'ab', 'names', 'denotes',
               'class', 'basic', 'symbols', 'development', 'algol', 'led',
               'algol', '60', 'committee', '1963', 'report', 'peter', 'naur',
               'called', 'backus', 'notation', 'backus', 'normal', 'form',
               'donald', 'knuth', 'argued', 'bnf', 'rather', 'read', 'backus',
               'naur', 'form', 'normal', 'form', 'conventional', 'sense',
               'unlike', 'instance', 'chomsky', 'normal', 'form', 'name',
               'panini', 'backus', 'form', 'also', 'suggested', 'view', 'fact',
               'expansion', 'backus', 'normal', 'form', 'may', 'accurate',
               'panini', 'independently', 'developed', 'similar', 'notation',
               'earlier']

if indexer.tokenize(test_document) != test_result:
    print("[test] tokenize document: failed")
    exit(1)

print("[test] indexer test: passed")
