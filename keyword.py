import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# Load spaCy's model
nlp = spacy.load("en_core_web_sm")
def query_parser(query):
    """
    Parses the user query to extract key terms, while handling stop words, lemmatization,
    and multi-word entities or phrases.
    :param query: User query string
    :return: List of cleaned, meaningful key terms
    """
    # Process the query using spaCy
    doc = nlp(query)
    # Extract key terms (lemmas) while removing stop words, punctuation, and irrelevant terms
    key_terms = []
    for token in doc:
        # Check if token is not a stop word, punctuation, or irrelevant term
        if token.text.lower() not in STOP_WORDS and not token.is_punct:
            # Only keep the lemmatized form of the token
            key_terms.append(token.lemma_.lower())
    print(f"Extracted Key Terms: {key_terms}")  # Debugging output
    return key_terms
