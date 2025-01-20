import streamlit as st
from keyword import query_parser
from retreive import retrieve_documents
from rank import rank_documents
from generate import generate_response
import pdfplumber


documents = [] 
# Load PDF documents
def load_documents(uploaded_files):
    global documents
    for uploaded_file in uploaded_files:
        document_text = ""
        if uploaded_file.type == "application/pdf":
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        document_text += page.extract_text() or ""
                if document_text.strip():
                    documents.append(document_text)
                    st.success(f"Document '{uploaded_file.name}' added successfully!")
                else:
                    st.warning(f"Document '{uploaded_file.name}' has extractable text.")
            except Exception as e:
                st.error(f"Error processing '{uploaded_file.name}': {e}")

# Streamlit app interface
st.set_page_config(page_title="Multi-Agent RAG System", layout="centered")

# Sidebar for document upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload multiple documents", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        load_documents(uploaded_files)


st.title("Multi-Agent- Retrieval Augmented Generation System")

# Query input
query = st.text_input("Enter your query:")

if query:
    
    key_terms = query_parser(query)
    

    st.subheader("Retrieved Documents")
    top_docs = retrieve_documents(key_terms)
    if top_docs:
        for i, (path, snippet, score) in enumerate(top_docs, start=1):
            st.write(f"Document {i}:{path}(Score: {score})")
    

            
    else:
        st.write("No relevant documents found.")

    
    ranked_docs = rank_documents(top_docs)
    
    # Generated Response Box
    st.subheader("Generated Response")
    response = generate_response(ranked_docs)
    
    st.markdown(f"""
    <div style="background-color:#f0f8ff; padding:10px; border-radius:10px;">
        <strong>Generated Response:</strong>
        <p style="font-size:18px; color:#333333;">{response}</p>
    </div>
    """, unsafe_allow_html=True)

# Additional Styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .stTextInput label {
        color: #4CAF50;
    }
    .stWrite>p {
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)
