def rank_documents(documents):
    """
    Ranks documents based on their relevance score.
    :param documents: List of tuples (document snippet, score)
    :return: List of ranked documents
    """
    ranked_docs = sorted(documents, key=lambda x: x[1], reverse=True)
    return ranked_docs
