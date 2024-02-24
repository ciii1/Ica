import parser
import indexer
import query
import sys
import os
import glob

documents_file_path = "data/doc"
pkl_file_path = "data/pkl"

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} [mode]")
    print("Modes:")
    print("\trun: run the program")
    print("\tindex: read the .doc files and save the indexed documents into .pkl files in data/")
    print("Not enough argument given, exiting...")
    sys.exit(0)

mode = sys.argv[1]

if mode == "run":
    indexer.load(pkl_file_path)
    input_query = ""
    while True:
        input_query = input("ica>>>")
        if input_query == "!exit":
            print("Bye.")
            break
        res_docs = query.query(input_query)
        if len(res_docs) == 0:
            print("")
        else:
            print(indexer.get_doc(res_docs[0].index))

elif mode == "index": 
    file_pattern = os.path.join(documents_file_path, f"*.doc")
    file_list = glob.glob(file_pattern)

    for file_path in file_list:
        file = open(file_path, 'r')
        parsed = parser.parse(file.read())
        indexer.index(parsed)

    indexer.save(pkl_file_path)
else:
    print("Mode '" + mode + "' is unrecognizable")
    sys.exit(0)
