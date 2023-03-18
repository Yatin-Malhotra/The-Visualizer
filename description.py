import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer as SumyTokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.utils import get_stop_words
from keybert import KeyBERT
from textblob import TextBlob
import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(certifi.where())

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def generate_description(text):
    # Step 1: Preprocessing, i.e., removing the non alpha numeric characters for the next steps
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha() and word not in stop_words]

    # Step 2: Lemmatization, i.e., reducing to the simpliest forms for analysis purposes
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Step 3: Part-of-Speech Tagging, i.e., assigning them if they are nouns, verbs, etc. 
    tagged_words = nltk.pos_tag(words)

    # Step 4: Text summarization, i.e., summarizing to gain a better understanding of the text
    summary = get_summary(text)

    # Step 5: Extracting keywords, i.e., getting the most important words that display the overall
    # meaning of the text
    keywords = get_keywords(summary)

    new_keywords = ' '.join(keywords[:3])
    already_in_keywords = []
    temp_arr = []

    temp_str = ""

    i = 0
    for i in range(len(new_keywords)):
        if (new_keywords[i] != ' '):
            temp_str += new_keywords[i]
        else:
            temp_arr.append(temp_str)
            temp_str = ""

    temp_arr.append(temp_str)

    for word in temp_arr:
        if word not in already_in_keywords:
            already_in_keywords.append(word)

    # Step 6: Generate a three-word description <- required for the future purepose of generating the
    # image
    description = ' '.join(already_in_keywords[:3])
    return description

def get_summary(text):
    # Use the LexRank algorithm from the sumy library to generate a summary of the input text
    parser = PlaintextParser(text, SumyTokenizer('english'))
    summarizer = LexRankSummarizer()
    summarizer.stop_words = get_stop_words('english')
    summary = summarizer(parser.document, sentences_count=5)
    summary = ' '.join(str(sentence) for sentence in summary)
    return summary

def get_keywords(text):
    # Use the KeyBERT algorithm to extract the most important multi-word phrases from the text
    model = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words=None)
    text_keywords = [keyword[0] for keyword in keywords]
    return text_keywords

# Get the sentimental index (required for the image processing)
def get_sentiments(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment
