import os
import glob

def convert_to_docs(articles): 
    output = ""
    parts = articles.split("\n===\n")
    is_first_iter = True
    for article in parts:
        paragraphs = article.split("\n\n")
        for paragraph in paragraphs[1:]:
            if not is_first_iter:
                output += "\n===\n"
            output += "<" + paragraphs[0] + ">" + "{" + paragraph + "}"
            is_first_iter = False
    return output

articles_file_path = "articles/"
file_pattern = os.path.join(articles_file_path, f"*.txt")
file_list = glob.glob(file_pattern)

for file_path in file_list:
    file = open(file_path, 'r')
    docs = convert_to_docs(file.read())
    w_file_name = os.path.splitext(os.path.basename(file_path))[0]
    w_file = open(w_file_name + ".doc", 'w')
    w_file.write(docs)
