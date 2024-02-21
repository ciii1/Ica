from parser import Node
from parser import NodeType
from dataclasses import dataclass
import re
import os
import pickle

__indexes = {}
"""
the global inverted index
"""

__case_insensitive_indexes = {}

__char_indexes = {}
"""
the indexes are a-z, normalized.
each index contains a map with the normalized keyword index as its key with its value as list of the index where the characters appear.
"""

#FIXME: use sqlite for this
__docs = []
"""
the documents/response templates
"""

@dataclass
class IndexValue:
    freq: int
    positions: list[int]

def index(ast):
    global __indexes
    global __docs

    for doc in ast:
        curr_doc = ""
        keywords = []
        for token in doc: 
            if token._type == NodeType.KEYWORD:
                keywords += extract_keywords(token.text)
            elif token._type == NodeType.CONTENT_KEYWORD:
                curr_doc += token.text
                keywords += extract_keywords(token.text)
            elif token._type == NodeType.CONTENT:
                curr_doc += token.text
        __docs.append(curr_doc)
        append_indexes(keywords, len(__docs)-1)

def append_indexes(keywords, doc_index):
    global __indexes
    global __case_insensitive_indexes
    global __char_indexes
    global __docs

    pos = 0
    for keyword in keywords:
        __indexes.setdefault(keyword, {})
        __indexes[keyword].setdefault(doc_index, IndexValue(freq=0, positions=[]))
        __indexes[keyword][doc_index].freq += 1
        __indexes[keyword][doc_index].positions.append(pos)
        normalized_keyword = keyword.lower()
        __case_insensitive_indexes.setdefault(normalized_keyword, [])
        if keyword not in __case_insensitive_indexes[normalized_keyword]:
            __case_insensitive_indexes[normalized_keyword].append(keyword)

        for char in normalized_keyword:
            __char_indexes.setdefault(char, [])
            if keyword not in __char_indexes[char]:
                __char_indexes[char].append(keyword)
            
        pos += 1

#FIXME: also remove words like and, then, etc. except if it's in the "header" or something
def extract_keywords(text):
    cleaned = re.sub(r'[^a-zA-Z \t\n]', '', text)
    splitted = cleaned.split()
    out = []
    for split in splitted:
        if split != "":
            out.append(split)
    return out

def get_index(index):
    global __indexes
    try: 
        return __indexes[index]
    except KeyError:
        return None

def get_case_insensitive_index(normalized_index):
    global __case_insensitive_indexes
    try: 
        return __case_insensitive_indexes[normalized_index]
    except KeyError:
        return None

def get_char_index(normalized_char):
    global __char_indexes
    try: 
        return __char_indexes[normalized_char]
    except KeyError:
        return None

def clear():
    global __indexes
    global __docs
    global __case_insensitive_indexes
    global __char_indexes
    __indexes = {}
    __case_insensitive_indexes = {}
    __char_indexes = {}
    __docs = []

def save(path):
    global __indexes
    global __docs
    global __case_insensitive_indexes
    global __char_indexes
    with open(os.path.join(path, "index.pkl"), 'wb') as file:
        pickle.dump(__indexes, file)
    with open(os.path.join(path, "docs.pkl"), 'wb') as file:
        pickle.dump(__docs, file)
    with open(os.path.join(path, "ci_index.pkl"), 'wb') as file:
        pickle.dump(__case_insensitive_indexes, file)
    with open(os.path.join(path, "ch_index.pkl"), 'wb') as file:
        pickle.dump(__char_indexes, file)

def load(path):
    global __indexes
    global __docs
    global __case_insensitive_indexes
    global __char_indexes
    with open(os.path.join(path, "index.pkl"), 'rb') as file:
        __indexes = pickle.load(file)
    with open(os.path.join(path, "docs.pkl"), 'rb') as file:
        __docs = pickle.load(file)
    with open(os.path.join(path, "ci_index.pkl"), 'rb') as file:
        __case_insensitive_indexes = pickle.load(file)
    with open(os.path.join(path, "ch_index.pkl"), 'rb') as file:
        __char_indexes = pickle.load(file)

def get_doc(index):
    global __docs
    return __docs[index]
