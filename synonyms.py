__synonyms = {
    'dumb': [
        'stupid', 
        'idiot',
    ],
    'stupid': [
        'dumb', 
        'idiot',
    ],
    'idiot': [
        'dumb', 
        'stupid',
    ],
}

def get(key):
    global __synonyms
    try:
        ret = __synonyms[key]
    except KeyError:
        ret = []
    return ret
