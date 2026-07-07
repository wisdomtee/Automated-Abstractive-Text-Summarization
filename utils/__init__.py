from pypdf import PdfReader
from docx import Document


def read_txt(uploaded_file):
    """
    Read a TXT file and return its contents.
    """
    return uploaded_file.read().decode("utf-8")


def read_pdf(uploaded_file):
    """
    Extract text from every page of a PDF.
    """
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def read_docx(uploaded_file):
    """
    Extract text from a Word document.
    """
    document = Document(uploaded_file)

    paragraphs = []

    for paragraph in document.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs).strip()


def extract_text(uploaded_file):
    """
    Automatically detect the uploaded file type
    and return the extracted text.
    """

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return read_txt(uploaded_file)

    elif filename.endswith(".pdf"):
        return read_pdf(uploaded_file)

    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)

    raise ValueError("Unsupported file format.")