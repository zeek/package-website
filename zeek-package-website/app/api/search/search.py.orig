from numpy import log as ln
from os import listdir


def get_avgdl(documents: []) -> int:
    avgdl = 0

    for document in documents:
        avgdl += len(document)

    return avgdl / len(documents)


def get_frequency(document: str, term: str) -> int:

    frequency = 0

    for word in document:
        if term in word:
            frequency += 1

    return frequency


def get_idfs(documents: [], query: []) -> dict:
    idfs = {}

    for term in query:
        idfs.update({term: get_idfs_helper(documents, term)})

    return idfs


def get_idfs_helper(documents: [], term: str) -> int:
    document_frequency = 0

    for document in documents:
        for word in document:
            if term in word.lower():
                document_frequency += 1

    return ln(((len(documents) - document_frequency + 0.5) /
               (document_frequency + 0.5)) + 1)


def rank(documents: [], query: str) -> []:
    scores = []
    query = query.lower().split()
    idfs = get_idfs(documents, query)
    avgdl = get_avgdl(documents)

    for document in documents:
        scores.append(score(document, query, avgdl, idfs))

    return scores


def score(document: [], query: [], avgdl: int, idfs: dict) -> int:
    score = 0

    for term in query:
        score += score_helper(document, term, avgdl, idfs)

    return score


def score_helper(document: str, term: str, avgdl: int, idfs: dict) -> int:

    frequency = get_frequency(document, term)
    idf = idfs.get(term)
    k1 = 1.0  # k1 is a free variable anywhere from 1.2 to 2
    b = 0.75  # b is a free variable that is commonly 0.75
    delta = 1.0  # delta is a free variable that is commonly 1.0
    score = ((frequency * (k1 + 1)) /
             (frequency + k1 * (1 - b + b * (len(document) / avgdl)))) + delta

    return idf * score


def search(query: str) -> list:
    """
    Returns a list of package file names sorted by relevane.
    
    Parameters
    ----------
    query : str
        The search query in the form of a string
        
    Returns
    -------
    list
        A sorted list of tuples where the first item is the name and the second is the score
    
    Examples
    --------
    >>> from search import search
    >>> query = "ja3"
    >>> results = search(query)
    >>> print(results)
    """
    documents = []
    document_names = listdir("json_files")

    for name in document_names:
        text_file = open(f"json_files/{name}", "r")
        data = text_file.read()
        data = data.split("readme")[1]
        data = data.lower().split()
        documents.append(data)
        text_file.close()

    rankings = rank(documents, query)

    rankings = {document_names[i]: rankings[i] for i in range(len(document_names))}

    return sorted(rankings.items(), key=lambda item: item[1], reverse=True)

def main():
    query = "ja3"

    print(f"The query is: {query}\n")

    results = search(query)
    print(f"Results: {results}\n")
    print(type(results[0]))


if __name__ == "__main__":
    main()
