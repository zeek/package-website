from numpy import log as ln


def rank(documents: [], query: str) -> []:
    scores = []
    query = query.lower().split()
    idfs = get_idfs(documents, query)
    avgdl = get_avgdl(documents)
    for document in documents:
        scores.append(score(document, query, avgdl, idfs))

    return scores


def get_avgdl(documents: []) -> int:
    avgdl = 0

    for document in documents:
        avgdl += len(document)

    return avgdl / len(documents)


def score(document: [], query: [], avgdl: int, idfs: dict) -> int:
    score = 0

    for term in query:
        score += score_helper(document, term, avgdl, idfs)

    return score


def score_helper(document: str, term: str, avgdl: int, idfs: dict) -> int:

    frequency = get_frequency(document, term)
    idf = idfs.get(term)
    k1 = 1.6  # k1 is a free value anywhere from 1.2 to 2
    b = 0.75  # b is a free value that is commonly 0.75

    score = ((frequency * (k1 + 1)) /
             (frequency + k1 * (1 - b + b * len(document) / avgdl)))

    return idf * score


def get_frequency(document: str, term: str) -> int:

    frequency = 0

    for word in document:
        if word.lower() == term:
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
        if term in document:
            document_frequency += 1

    return ln(((len(documents) - document_frequency + 0.5) /
               (document_frequency + 0.5)) + 1)


def search(query: str) -> dict:

    documents = []
    document_names = ["example1.txt", "example2.txt", "example3.txt"]

    for name in document_names:
        text_file = open(name, "r")
        data = text_file.read()
        data = data.lower().split()
        documents.append(data)
        text_file.close()

    rankings = rank(documents, query)

    return {document_names[i]: rankings[i] for i in range(len(document_names))}


def main():
    query = "yellow cat"

    print(f"The query is: {query}\n")

    print(f"Results: {search(query)}\n")


if __name__ == "__main__":
    main()
