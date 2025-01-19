from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_response(top_documents):
    """
    Generates a response based on top-ranked documents.
    :param top_documents: List of top-ranked document snippets
    :return: Generated summary text
    """
    if not top_documents:
        return "No documents available to generate a response."
    
    # Combine document snippets into a single string
    # Combine document snippets (second value in each tuple) into a single string
    combined_text = " ".join([doc[1] for doc in top_documents if isinstance(doc[1], str)])

    
    # Ensure the combined text does not exceed token limit for BART (typically 1024 tokens)
    max_length = 1024
    if len(combined_text.split()) > max_length:
        combined_text = " ".join(combined_text.split()[:max_length])
    
    try:
        # Summarize the combined text
        response = summarizer(combined_text, max_length=40, min_length=10, do_sample=False)
        return response[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {e}"
