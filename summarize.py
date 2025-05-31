import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
nltk.data.path.append('/Users/apple/nltk_data')  # or the correct path to your NLTK data
nltk.download('punkt', quiet=True)
import pdfplumber
# from gensim.summarization import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer



from nltk.tokenize import sent_tokenize
text = "This is a sentence. Here's another one."
sentences = sent_tokenize(text)
print(sentences)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    page_texts = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                  # Print first 500 characters of each page
                page_texts.append(page_text)
    return page_texts

    

# Function to summarize the text

def summarize_text(page_texts):
    summaries = []
    summarizer = LsaSummarizer() 

    # Loop through each page's text and summarize it individually
    for page_text in page_texts:
        if page_text.strip():  # If the page has text
            parser = PlaintextParser.from_string(page_text, Tokenizer("english"))
            summary = summarizer(parser.document, sentences_count=6)  # Adjust sentence count per page if needed
            summaries.append(' '.join([str(sentence) for sentence in summary]))
        else:
            summaries.append('')  # If the page is blank, append an empty string
    return summaries  # Return a list of summaries, one for each page