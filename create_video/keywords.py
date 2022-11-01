import nltk
import nltk.data
from nltk import tokenize

from rake_nltk import Rake
rake_nltk_var = Rake()

nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def keywords(content):
    #tokenize_summary = tokenize.sent_tokenize(content)
    rake_nltk_var.extract_keywords_from_text(content)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()

    #print(keyword_extracted)

    return keyword_extracted

