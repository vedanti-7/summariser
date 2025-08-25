from flask import Flask, render_template, request, send_file
from summarize import extract_text_from_pdf, summarize_text
from fpdf import FPDF
import os
import nltk

# Ensure nltk uses local folder for deployment
nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_dir)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files['pdf']
    page_texts = extract_text_from_pdf(pdf_file)
    summaries = summarize_text(page_texts)
    summary_pdf = create_summary_pdf(summaries)
    return send_file(summary_pdf, as_attachment=True, download_name='summary.pdf')

def create_summary_pdf(summaries):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, summary in enumerate(summaries):
        pdf.add_page()
        cleaned_summary = summary.encode('utf-8', 'replace').decode('utf-8')
        pdf.multi_cell(0, 10, f"Summary of Page {i+1}:\n{cleaned_summary}")

    summary_pdf_path = 'summary.pdf'
    pdf.output(summary_pdf_path)
    return summary_pdf_path

if __name__ == '__main__':
    app.run(debug=True)