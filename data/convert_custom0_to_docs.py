import os
import glob

def convert_to_docs(text):
    splits = text.split("\n===\n")
    out = ""
    for part in splits:
        lines = part.split("\n")
        is_first_iter = True
        is_question = True
        context_questions = ""
        for line in lines:
            if is_question:
                if not is_first_iter:
                    out += "\n===\n"
                out += context_questions + "<2" + line[2:] + ">"
                context_questions += "<" + line[2:] + ">"
            else:
                out += "[" + line[2:] + "]"

            if is_question:
                is_question = False
            else:
                is_question = True
            is_first_iter = False
    return out

articles_file_path = "custom0/"
output_file_path = "doc"
file_pattern = os.path.join(articles_file_path, f"*.txt")
file_list = glob.glob(file_pattern)

for file_path in file_list:
    file = open(file_path, 'r')
    docs = convert_to_docs(file.read())
    w_file_name = os.path.splitext(os.path.basename(file_path))[0]
    with open(os.path.join(output_file_path, w_file_name + ".doc"), 'w') as w_file:
        w_file.write(docs)
