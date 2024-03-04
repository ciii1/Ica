# Currently, this file only supports html files from wikipedia.org

import bs4
from bs4 import BeautifulSoup
import re
import os
import glob

MAX_PARAGRAPH_DISTANCE = 30

def convert_to_html(html_doc):
    out = ""
    soup = BeautifulSoup(html_doc, 'html.parser')
    is_first_iter = True
    used_titles = []
    last_paragraph = None
    for paragraph in soup.find_all("p"):
        previous_element = paragraph.previous_element
        while previous_element != None:
            if previous_element in used_titles:
                previous_element = None
                break
            if type(previous_element) == bs4.element.Tag and previous_element.name in ["h1", "h2", "h3", "h4", "h5"]: 
                used_titles.append(previous_element)
                break
            previous_element = previous_element.previous_element
    
        if previous_element:
            title = re.sub(r'([\n\t]|(  ))+', ' ', previous_element.get_text())
            title = re.sub(r'(  )+', ' ', title)
            title = re.sub(r' \)', ')', title)
            title = re.sub(r' ,', ',', title)
            title = re.sub(r'\( ', '(', title)
            title = re.sub(r'\[', '\[', title)
            title = re.sub(r'\]', '\]', title)
            title = re.sub(r'\{', '\{', title)
            title = re.sub(r'\}', '\}', title)
            title = re.sub(r'\<', '\<', title)
            title = re.sub(r'\>', '\>', title)
            if not is_first_iter:
                out += "]\n===\n"
            else:
                is_first_iter = False
            out += "{2" + title + "\n}"
            out += "["
        else:
            i = 0
            p = paragraph.previous_element
            while p != None:
                if p == last_paragraph: 
                    break
                p = p.previous_element
                i += 1
            if p == None or i > MAX_PARAGRAPH_DISTANCE:
                continue
    
        text = re.sub(r'([\n\t]|(  ))+', ' ', paragraph.get_text())
        text = re.sub(r'(  )+', ' ', text)
        text = re.sub(r' \)', ')', text)
        text = re.sub(r' ,', ',', text)
        text = re.sub(r'\( ', '(', text)
        text = re.sub(r'\[[0-9]+ \]', '', text)
        text = re.sub(r'\[', '\[', text)
        text = re.sub(r'\]', '\]', text)
        text = re.sub(r'\{', '\{', text)
        text = re.sub(r'\}', '\}', text)
        text = re.sub(r'\<', '\<', text)
        text = re.sub(r'\>', '\>', text)
        out += text + "\n"
        last_paragraph = paragraph
    out += "]\n"
    print(out)
    return out

articles_file_path = "articles/"
output_file_path = "doc"
file_pattern = os.path.join(articles_file_path, f"*.html")
file_list = glob.glob(file_pattern)

for file_path in file_list:
    file = open(file_path, 'r')
    docs = convert_to_html(file.read())
    w_file_name = os.path.splitext(os.path.basename(file_path))[0]
    with open(os.path.join(output_file_path, w_file_name + ".doc"), 'w') as w_file:
        w_file.write(docs)

