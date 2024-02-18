from parser import Node
from parser import NodeType
import re

__indices = {}
"""
the global inverted index
"""

#FIXME: use sqlite for this
__docs = []
"""
the documents/response templates
"""

def index(ast):
    global __indices
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
        append_indices(keywords, len(__docs))
        __docs.append(curr_doc)

def append_indices(keywords, doc_index):
    global __indices

    for keyword in keywords:
        __indices.setdefault(keyword, {})
        __indices[keyword].setdefault(doc_index, 0)
        __indices[keyword][doc_index] += 1

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
    global __indices
    try: 
        return __indices[index]
    except KeyError:
        return None

def clear():
    global __indices
    global __docs
    __indices = {}
    __docs = []
