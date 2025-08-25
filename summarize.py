import nltk
import os

# Create a local nltk_data folder inside your project (for deployment)
nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Add the local folder to NLTK's path
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data if missing
for resource in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource, download_dir=nltk_data_dir, quiet=True)

from nltk.tokenize import sent_tokenize
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Example test
text = "This is a sentence. Here's another one."
sentences = sent_tokenize(text)
print(sentences)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    page_texts = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                page_texts.append(page_text)
    return page_texts

# Function to summarize text
def summarize_text(page_texts):
    summaries = []
    summarizer = LsaSummarizer()
    for page_text in page_texts:
        if page_text.strip():
            parser = PlaintextParser.from_string(page_text, Tokenizer("english"))
            summary = summarizer(parser.document, sentences_count=6)
            summaries.append(' '.join([str(sentence) for sentence in summary]))
        else:
            summaries.append('')
    return summaries