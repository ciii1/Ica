from parser import Node
from parser import NodeType
from dataclasses import dataclass
import re
import os
import pickle
import math
import stopwords

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
    weight: int
    positions: list[int]

@dataclass
class Keyword:
    text: str
    section_weight: float

def index(ast):
    global __indexes
    global __docs

    for doc in ast:
        curr_doc = ""
        keywords = []
        for token in doc: 
            if token._type == NodeType.KEYWORD:
                keywords += extract_keywords(token.text, token.weight)
            elif token._type == NodeType.CONTENT_KEYWORD:
                curr_doc += token.text
                keywords += extract_keywords(token.text, token.weight)
            elif token._type == NodeType.CONTENT:
                curr_doc += token.text
        __docs.append(curr_doc)
        append_indexes(keywords, len(__docs)-1)

def append_indexes(keywords, doc_index):
    global __indexes
    global __case_insensitive_indexes
    global __char_indexes
    global __docs

    max_section_weights = {}
    pos = 0
    for keyword in keywords:
        keyword_text = keyword.text

        max_section_weights.setdefault(keyword_text, 0);
        if keyword.section_weight > max_section_weights[keyword_text]:
            max_section_weights[keyword_text] = keyword.section_weight

        __indexes.setdefault(keyword_text, {})
        __indexes[keyword_text].setdefault(doc_index, IndexValue(weight=0, positions=[]))
        __indexes[keyword_text][doc_index].weight = 1
        __indexes[keyword_text][doc_index].positions.append(pos)
        normalized_keyword = keyword_text.lower()
        __case_insensitive_indexes.setdefault(normalized_keyword, [])
        if keyword_text not in __case_insensitive_indexes[normalized_keyword]:
            __case_insensitive_indexes[normalized_keyword].append(keyword_text)

        for char in normalized_keyword:
            __char_indexes.setdefault(char, [])
            if keyword_text not in __char_indexes[char]:
                __char_indexes[char].append(keyword_text)
            
        pos += 1
    for keyword in keywords:
        keyword_text = keyword.text
        __indexes[keyword_text][doc_index].weight *= max_section_weights[keyword_text]

def extract_keywords(text, section_weight):
    cleaned = re.sub(r'[^a-zA-Z \t\n]', '', text)
    splitted = cleaned.split()
    out = []
    for split in splitted:
        if split in stopwords.list_ and section_weight < 2:
            continue
        elif split != "":
            out.append(Keyword(split, section_weight))
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
