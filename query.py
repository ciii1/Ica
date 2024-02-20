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
    
    last_docs = None
    for token in tokens:
        most_matching_case_insensitive = calculate_most_matching_case_insensitive(token)
        if most_matching_case_insensitive == None:
            continue
        docs = indexer.get_index(most_matching_case_insensitive.matched_index)
        for doc_index in docs:
            potential_docs.setdefault(doc_index, ResDocs(doc_index, 0)) 
            freq = docs[doc_index].freq
            #FIXME:add fuzzy search
            #proximity scoring
            proximity = 1
            if last_docs and doc_index in last_docs:
                closest_pos = find_closest_elements(docs[doc_index].positions, last_docs[doc_index].positions)
                raw_proximity = abs(closest_pos[0] - closest_pos[1])
                proximity = (raw_proximity / 100)+1  
            last_docs = docs

            potential_docs[doc_index].score += freq / (most_matching_case_insensitive.distance + 1) / proximity

    #divide score of the docs by 2 for every token of the query they don't contain
    for doc_index in potential_docs:
        for token in tokens:
            most_matching_case_insensitive = calculate_most_matching_case_insensitive(token)
            if most_matching_case_insensitive == None:
                potential_docs[doc_index].score /= 2
            else:
                docs = indexer.get_index(most_matching_case_insensitive.matched_index)
                if doc_index not in docs:
                    potential_docs[doc_index].score /= 2

    out = []
    for doc in potential_docs:
        out.append(potential_docs[doc])

    out = sorted(out, key=lambda x: x.score, reverse=True)
    return out

def find_closest_elements(arr1, arr2):
    min_difference = float('inf')
    closest_pair = (None, None)

    for num1 in arr1:
        for num2 in arr2:
            difference = abs(num1 - num2)
            if difference < min_difference:
                min_difference = difference
                closest_pair = (num1, num2)

    return closest_pair

@dataclass
class IndexCalculationRes:
    matched_index:str
    distance:float

def calculate_most_matching_case_insensitive(keyword):
    normalized_keyword = keyword.lower()
    indexes = indexer.get_case_insensitive_index(normalized_keyword)
    if indexes == None:
        return None
    least_distance = 10000
    most_matching = ""
    for index in indexes:
        local_distance = 0
        i = 0
        while i < len(keyword):
            if keyword[i] != index[i]:
                local_distance += 1
            i += 1
        if local_distance < least_distance:
            least_distance = local_distance
            most_matching = index
    
    return IndexCalculationRes(most_matching, normalize_distance(least_distance))

def normalize_distance(number):
    if number == 0:
        return 0
    # Count the number of digits
    num_digits = len(str(number))

    # Calculate the divisor as 10 raised to the power of the number of digits
    divisor = 10 ** num_digits

    # Transform the number to a float by dividing by the divisor
    result = number / divisor

    return result

def tokenize(text):
    cleaned = re.sub(r'[^a-zA-Z \t\n]', '', text)
    splitted = cleaned.split()
    out = []
    for split in splitted:
        if split != "":
            out.append(split)
    return out

