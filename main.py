import parser
import indexer
import query
import sys

documents_file_path = "data/"

if len(sys.argv) < 2:
    print("Usage: Ica [mode]")
    print("Modes:")
    print("\trun: run the program")
    print("\tindex: read the .doc files and save the indexed documents into .pkl files in data/")
    print("Not enough argument given, exiting...")
    sys.exit(0)

mode = sys.argv[1]

if mode == "run":
    indexer.load(documents_file_path)
    query = ""
    while query != "exit":
        input_query = input("ica$ ")
        res_docs = query.query(input_query)
        if len(res_docs) == 0:
            print("")
        else:
            res_docs[0]

elif mode == "index": 
    file_pattern = os.path.join(documents_file_path, f"*.doc")
    file_list = glob.glob(file_pattern)

    for file_path in file_list:
        file = open(file_path, 'r')
        parsed = parser.parse(file.read())
        indexer.index(parsed)

    indexer.save(documents_file_path)
else:
    print("Mode '" + mode + "' is unrecognizable")
    sys.exit(0)
