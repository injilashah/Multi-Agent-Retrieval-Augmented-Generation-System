import faiss
import os
from sentence_transformers import SentenceTransformer
from ner import query_parser  # Import the improved query parser
import pdfplumber
# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index
index = faiss.read_index("document_index.faiss")




file_path = 'I:/genaii/content/genai/documents'  # Path where your PDF documents are stored
documents = []
doc_paths = []

for file_name in os.listdir(file_path):
    # Check if the file is a PDF
    if file_name.endswith('.pdf'):
        with pdfplumber.open(os.path.join(file_path, file_name)) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Add text only if it's not None
                    text += page_text
            # Add the complete text from this PDF to the documents list and its path
            documents.append(text)
            doc_paths.append(file_name)
def retrieve_documents(key_terms, k=3):
    """
    Searches the document database for relevant files based on the extracted key terms and query.
    :param query: User query string
    :param documents: List of document texts
    :param k: Number of top results to return
    :return: List of tuples [(document_path, document_snippet, distance)]
    """
    
   
    query_embedding = model.encode([key_terms])

    # Step 3: Perform search using FAISS
    distances, indices = index.search(query_embedding, k)

    # Step 4: Prepare the results
    results = []
    for i in range(k):
        doc_index = indices[0][i]  # Get the index of the retrieved document
        document_snippet = documents[doc_index][:]  # Get the first 200 characters as a snippet
        document_path = doc_paths[doc_index]  # Retrieve the document path or title
        distance = distances[0][i]  # Similarity score
        distance = round(distance, 2)
        # Append to the results as a tuple
        results.append((document_path, document_snippet, distance))

    return results
