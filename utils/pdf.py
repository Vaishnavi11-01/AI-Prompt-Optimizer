from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    Returns the extracted text as a string.
    """
    try:
        pdf_reader = PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Extract text from PDF bytes.
    Returns the extracted text as a string.
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        return extract_text_from_pdf(pdf_file)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF bytes: {str(e)}")
