import os
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import re
file_path = 'I:/genaii/content/genai/documents'  # Path where PDF documents are stored
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
# Check if documents are loaded
if not documents:
    raise ValueError("No documents were loaded. Ensure the folder contains valid PDF files.")





# Preprocess Documents (tokenization and cleaning)
def preprocess_text(text):
    # Tokenize and clean text (remove special characters and unnecessary spaces)
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
    return text.strip()
documents = [preprocess_text(doc) for doc in documents]

#  Generate Embeddings using Sentence-Transformer
model = SentenceTransformer('all-MiniLM-L6-v2')  
embeddings = model.encode(documents)
# Store embeddings in FAISS
dimension = embeddings.shape[1]  # Get the embedding dimension
index = faiss.IndexFlatL2(dimension)  # Create a FAISS index 
index.add(embeddings)  # Add embeddings to the index
# Save the FAISS index to a file
faiss.write_index(index, "document_index.faiss")


