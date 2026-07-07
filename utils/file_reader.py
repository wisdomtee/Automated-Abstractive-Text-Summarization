import PyPDF2
from docx import Document


def extract_text(uploaded_file):

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "txt":
        return uploaded_file.read().decode("utf-8")

    elif extension == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text

    elif extension == "docx":
        doc = Document(uploaded_file)

        return "\n".join(
            paragraph.text 
            for paragraph in doc.paragraphs
        )

    else:
        return ""