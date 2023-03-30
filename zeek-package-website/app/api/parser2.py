import re


def parse(file):
    with open(file, 'r') as f:
        contents = f.read()

    # Find all matches of the regular expression in the file contents
    matches = re.findall(
        r'\[[^/^][^[]*?\/[^[]*?\][^[]*',
        contents,
        flags=re.DOTALL)

    # Initialize a list to store the results
    results = []

    # Loop over each match and extract the desired fields
    for match in matches:
        # Extract the section header
        section_header = re.search(r'\[[^/^].*?\/[^[]*?\]', match).group(0)

        # Extract the description
        description_match = re.search(
            r'^description\s*=\s*(.+)', match, flags=re.MULTILINE)
        if description_match:
            description = description_match.group(1)

            # Append the section header and description as a tuple to the
            # results list
            results.append((section_header, description))

    # Return the list of results
    return results


def main():
    file = 'aggregate.meta'
    results = parse(file)

    # loop thru results list for the tuples within
    for section_header, description in results:
        print(section_header)
        print(description)
        print()  # Print a blank line between entries


if __name__ == '__main__':
    main()
