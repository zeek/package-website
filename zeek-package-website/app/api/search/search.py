from numpy import log as ln
import os


def bias(rankings: dict, query: str):
    new_list = []

    if(rankings is None or query is None):
        return None

    for item in rankings.items():
        if query in item[0].split(".")[0]:
            new_item = (item[0], item[1] + 3.0)
            new_list.append(new_item)
        else:
            new_list.append(item)

    return new_list


def get_avgdl(documents: []) -> int:
    avgdl = 0

    for document in documents:
        avgdl += len(document)

    return avgdl / len(documents)


def get_frequency(document: str, term: str) -> int:

    frequency = 0

    for word in document:
        if term in word and not (word.startswith("http://") or word.startswith("https://")):
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
            if term in word.lower() and not ("http://" in word or "https://" in word):
                document_frequency += 1

    return ln(((len(documents) - document_frequency + 0.5) / (document_frequency + 0.5)) + 1)


def get_lower_bound(rankings: list) -> int:

    if rankings is None:
        return None

    index = 0
    min_val = min(set(x[1] for x in rankings))
    while rankings[index][1] > min_val:
        index += 1

    return index


def rank(documents: [], query: str) -> []:
    scores = []
    query = query.lower().split()

    if documents is None:
        raise TypeError

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
    score = ((frequency * (k1 + 1)) / (frequency + k1 * (1 - b + b * (len(document) / avgdl)))) + delta

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
    project_dir = os.path.dirname(os.path.abspath(__file__))
    json_files_dir = os.path.join(project_dir, "json_files")
    document_names = os.listdir(json_files_dir)
    for name in document_names:
        text_file = open(os.path.join(json_files_dir, name), "r")
        data = text_file.read()
        data = data.split("readme")[1]
        data = data.lower().split()
        documents.append(data)
        text_file.close()

    rankings = rank(documents, query)

    rankings = {document_names[i]: rankings[i] for i in range(len(document_names))}

    rankings = bias(rankings, query)

    rankings = sorted(rankings, key=lambda item: item[1], reverse=True)

    return rankings[0:get_lower_bound(rankings)]


def main():
    query = "ssh"

    print(f"The query is: {query}\n")

    results = search(query)
    print(f"Results: {results}\n")


if __name__ == "__main__":
    main()
