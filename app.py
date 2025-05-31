import nltk
nltk.download('punkt')
nltk.data.path.append('/Users/apple/nltk_data')  # or the correct path to your NLTK data
nltk.download('punkt', quiet=True)
print(nltk.data.path)

from flask import Flask, render_template, request, send_file
import os
from summarize import extract_text_from_pdf, summarize_text
# from fpdf import FPDF
from fpdf import FPDF

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle PDF upload and summarization
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files['pdf']
    
    # Extract text from the uploaded PDF (page by page)
    page_texts = extract_text_from_pdf(pdf_file)
    
    # Summarize the extracted text (summarize each page separately)
    summaries = summarize_text(page_texts)
    
    # Generate a new summarized PDF, page by page
    summary_pdf = create_summary_pdf(summaries)
    
    # Return the summarized PDF to the user
    return send_file(summary_pdf, as_attachment=True, download_name='summary.pdf')

# Function to create a PDF from the summarized text
def create_summary_pdf(summaries):
    pdf = FPDF()
    pdf.add_page()

     # Add a Unicode font (make sure you have the .ttf file)
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)  # Ensure the 'fonts' directory has the DejaVuSans.ttf file
    pdf.set_font('DejaVu', size=12)  # Use Unicode font

    pdf.set_auto_page_break(auto=True, margin=15)  # Optional: Handle automatic page breaks
    # pdf.set_font("Arial", size=12)

    # Loop through each page's summary and add it to the PDF
    for i, summary in enumerate(summaries):
        pdf.add_page()
        # Replace invalid characters and ensure text encoding is safe for PDF generation
        cleaned_summary = summary.encode('utf-8', 'replace').decode('utf-8')
        pdf.multi_cell(0, 10, f"Summary of Page {i+1}:\n{cleaned_summary}")
    
    # Save the PDF to a temporary file
    summary_pdf_path = 'summary.pdf'
    pdf.output(summary_pdf_path)
    return summary_pdf_path

if __name__ == '__main__':
    app.run(debug=True)