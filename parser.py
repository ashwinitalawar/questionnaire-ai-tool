import pdfplumber


def extract_questions(file):

    questions = []

    # -------- PDF --------
    if file.name.endswith(".pdf"):

        with pdfplumber.open(file) as pdf:

            text = ""

            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        questions = [q.strip() for q in text.split("\n") if q.strip()]

    # -------- TXT --------
    elif file.name.endswith(".txt"):

        text = file.read().decode("utf-8")
        questions = [q.strip() for q in text.split("\n") if q.strip()]

    return questions