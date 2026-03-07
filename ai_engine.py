from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_vector_store(reference_files):

    documents = []
    filenames = []

    for file in reference_files:
        try:
            text = file.read().decode("utf-8", errors="ignore")
            documents.append(text)
            filenames.append(file.name)
        except Exception:
            continue

    vectorizer = TfidfVectorizer(stop_words="english")

    matrix = vectorizer.fit_transform(documents)

    vector_store = {
        "vectorizer": vectorizer,
        "matrix": matrix,
        "documents": documents,
        "filenames": filenames
    }

    return vector_store


def generate_answer(question, vector_store):

    vectorizer = vector_store["vectorizer"]
    matrix = vector_store["matrix"]
    documents = vector_store["documents"]
    filenames = vector_store["filenames"]

    question_vec = vectorizer.transform([question])

    similarities = cosine_similarity(question_vec, matrix)

    best_index = similarities.argmax()
    best_score = similarities[0][best_index]

    confidence = round(best_score * 100, 2)

    # If similarity too low → not found
    if best_score < 0.25:
        return "Not found in references.", "", confidence

    # Extract a useful snippet instead of whole document
    document_text = documents[best_index]

    snippet = document_text[:300]

    citation = filenames[best_index]

    return snippet, citation, confidence
