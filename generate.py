from transformers import pipeline, BartTokenizer

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def generate_response(top_documents):
    """
    Generates a response based on top-ranked documents.
    :param top_documents: List of top-ranked document snippets
    :return: Generated summary text
    """
    # Validate top_documents format
    if not all(isinstance(doc, tuple) and len(doc) > 1 and isinstance(doc[1], str) for doc in top_documents):
        return "Invalid input format for top documents."
    
    # Combine document snippets into a single string
    combined_text = " ".join([doc[1] for doc in top_documents if isinstance(doc[1], str)])
    
    # Ensure the combined text is not empty
    if not combined_text.strip():
        return "No valid content to summarize."

    # Truncate combined_text based on token limits
    tokens = tokenizer(combined_text, return_tensors="pt", truncation=True, max_length=1024)
    input_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
    
    try:
        # Summarize the input text
        response = summarizer(input_text, max_length=500, min_length=100, do_sample=False)
        return response[0]['summary_text']
    except IndexError as e:
        return "Summarization failed due to input size or format issue. Please check the input."
    except Exception as e:
        return f"Unexpected error during summarization: {e}"
