#Take the user query
query = input("Enter your query here: ")

#vector Similarity Search [Query] in DB
search_results = vector_db.similarity_search(
    query = query,
    )