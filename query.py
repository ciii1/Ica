from dataclasses import dataclass
from parser import NodeType
import stopwords
import Levenshtein
import math
import re
import indexer

@dataclass
class ResDocs:
    index:int
    score:float

def query(text):
    tokens = tokenize(text)
    potential_docs = {}
    

    is_non_stopwords_exist = False
    for token in tokens:
        if token not in stopwords.list_:
            is_non_stopwords_exist = True 

    if not is_non_stopwords_exist:
        token.append("usage")

    last_docs = None
    for token in tokens:
        most_matching = calculate_most_matching_case_insensitive(token)
        if most_matching == None:
            most_matching = calculate_most_matching_index(token)
            if most_matching == None:
                continue
        docs = indexer.get_index(most_matching.matched_index)
        for doc_index in docs:
            potential_docs.setdefault(doc_index, ResDocs(doc_index, 0)) 
            weight = docs[doc_index].weight

            #proximity scoring
            distance = 1
            if last_docs and doc_index in last_docs:
                closest_pos = find_closest_elements(docs[doc_index].positions, last_docs[doc_index].positions)
                raw_distance = abs(closest_pos[0] - closest_pos[1])  
                distance = (raw_distance / 100) + 1
            last_docs = docs
            
            potential_docs[doc_index].score += weight / (most_matching.distance + 1) / distance

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
    least_distance = float("inf")
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

@dataclass
class IndexCalculationResArray:
    matched_indexes:list
    score:float

def calculate_most_matching_index(keyword):
    normalized_keyword = keyword.lower()

    #get all the possibilities
    possible_keywords = []
    for char in normalized_keyword:
        indexes_pos = indexer.get_char_index(char)
        if indexes_pos == None:
            continue
        possible_keywords.append(indexes_pos)

    #narrow the possibilities
    possibilities = []
    for base_keyword in possible_keywords:
        possibility = []
        score = 0
        for p_keyword2 in possible_keywords:
            removed = remove_unique(base_keyword, p_keyword2)
            if len(removed) > 0:
                possibility = removed
                score += 1
        possibilities.append(IndexCalculationResArray(possibility, score))

    #get max score
    max_score = 0
    for possibility in possibilities:
        if possibility.score > max_score:
            max_score = possibility.score
    if max_score == 0:
        return None

    #get the best possibilities of possibility
    final = []
    for possibility in possibilities:
        if possibility.score == max_score:
            final.append(possibility.matched_indexes)
   
    #get the best keyword of keyword possibilities
    min_score = float("inf")
    best_match = ""
    for possibility in final:
        for p_keyword in possibility:
            score = Levenshtein.distance(p_keyword.lower(), normalized_keyword)
            if score < min_score:
                best_match = p_keyword
                min_score = score

    #is below the minimum levenshtein distance 
    if min_score > math.ceil(len(keyword) / 3) - 1:
        return None

    return IndexCalculationRes(best_match, normalize_distance(min_score))

def remove_unique(base, target):
    out = []
    for elem in target:
        if elem in base:
            out.append(elem)
    return out

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

