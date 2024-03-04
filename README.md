# Ica
At its core, Ica is a small search engine written in python, designed to be flexible and hackable. Superficially, it can also be a chatbot, autocompletion engine, etc.
In order to achieve the desired flexibility, it uses a custom algorithm, which is basically the lite version of BM25.

## Usage
```
git clone https://github.com/ciii1/ica/
cd ica
pip install requirements.txt
```
Next, you're ready to use ica. Run with
```
python3 main.py run
```
Though, it won't be much of use untill you start populating the `data/` directory, which is to be explained in the next section.

### Feeding data
The main task of a search engine is to retrieve documents or data that are relevant to the query provided by the user. It only makes sense if we need to feed the documents or data to the search engine first in order to be able to use it. For consistency, we'll start to call it data.

Data are placed under the directory `data/doc` with .doc extension. Ica has a simple but powerful system to define a document.
There are three types of section of a document in Ica:
 - The keyword: not displayed in the result but used in search.
 - The content: displayed in the result but not used in search.
 - The keyword and the content: used in search and also displayed in result
Each sections can be declared multiple times in a document. To declare a keyword, the following syntax is used:
```
<the text within that is supposed to be the keywords>
```
and as for content:
```
[the text within that is supposed to be the content]
```
and keyword and content:
```
{the text that is the keywords and the content}
```
Each section can have a custom weight applied to them. In order to do it, you simply have to specify the floating point that supposed to be its weight right after the opening bracket. For example:
```
{2the overall weight of the keyword here is multiplied by two}
```

To convert a file to ica document, a script can be used. Some sample scripts are placed under the `data/` directory. 
Once you're done feeding the documents. Index them with:
```
python3 main.py index
```

### Stopwords
Stopwords are words that are not included in the search. Though, in Ica, if a query only consists of stopwords then the stopwords will be used regardless. Stopwords can be defined in the file `stopwords.py`

### Synonyms
The indexer also use the synonym of a word if the word is used in a document. Synonyms can be defined in the file `synonyms.py`

## Speech support
The branch speech has support for speech recognition and text to speech. It uses vosk and festival with voice\_cmu\_us\_slt\_arctic\_hts.
