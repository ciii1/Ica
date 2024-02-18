from dataclasses import dataclass
from parser import NodeType
import re
import indexer

@dataclass
class ResDocs:
    index:int
    score:float

def query(text):
    tokens = tokenize(text)
    potential_docs = {}

    for token in tokens:
        docs = indexer.get_index(token)
        if docs == None:
            continue
        for doc_index in docs:
            potential_docs.setdefault(doc_index, ResDocs(doc_index, 0)) 
            freq = docs[doc_index]
            potential_docs[doc_index].score += freq

    for doc_index in potential_docs:
        for token in tokens:
            docs = indexer.get_index(token)
            if docs == None or doc_index not in docs:
                potential_docs[doc_index].score /= 2

    out = []
    for doc in potential_docs:
        out.append(potential_docs[doc])

    out = sorted(out, key=lambda x: x.score, reverse=True)
    return out

def tokenize(text):
    cleaned = re.sub(r'[^a-zA-Z \t\n]', '', text)
    splitted = cleaned.split()
    out = []
    for split in splitted:
        if split != "":
            out.append(split)
    return out

