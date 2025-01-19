import os
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import re

# Step 1: Extract text from PDFs
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

# Check if documents are loaded
if not documents:
    raise ValueError("No documents were loaded. Ensure the folder contains valid PDF files.")

# Step 2: Preprocess Documents (tokenization and cleaning)
def preprocess_text(text):
    # Tokenize and clean text (remove special characters and unnecessary spaces)
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
    return text.strip()

documents = [preprocess_text(doc) for doc in documents]

# Step 3: Generate Embeddings using Sentence-Transformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use any other Sentence Transformer model
embeddings = model.encode(documents)

# Step 4: Store embeddings in FAISS
dimension = embeddings.shape[1]  # Get the embedding dimension
index = faiss.IndexFlatL2(dimension)  # Create a FAISS index (L2 distance for similarity)
index.add(embeddings)  # Add embeddings to the index

# Save the FAISS index to a file
faiss.write_index(index, "document_index.faiss")

# Print summary
print(f"Processed {len(documents)} documents.")
print("FAISS index saved as 'document_index.faiss'.")
# Query Example: "Smart Wheelchair Design"
query = "Smart Wheelchair Design"
query_embedding = model.encode([query])

# Perform search
k = 5  # Number of top documents to retrieve
distances, indices = index.search(query_embedding, k)

# Output the results
print(f"Top {k} documents for query '{query}':")
for i in range(k):
    doc_index = indices[0][i]
    print(f"Document {i+1}: {doc_paths[doc_index]}, Distance: {distances[0][i]}")