import re


def parse(file):
    with open(file, 'r') as f:
        contents = f.read()

# Find all matches of the regular expression in the file contents
    matches = re.findall(
        r'\[[^/^][^[]*?\/[^[]*?\][^[]*',
        contents,
        flags=re.DOTALL)

# Loop over each match and extract the desired fields
    for match in matches:
        # Extract the section header
        section_header = re.search(r'\[[^/^].*?\/[^[]*?\]', match).group(0)

        # Extract the description
        description_match = re.search(
            r'^description\s*=\s*(.+)', match, flags=re.MULTILINE)
        if description_match:
            description = description_match.group(1)

            # Print the section header and description
            print(section_header)
            print(description)
            print()  # Print a blank line between entries


def main():
    file = 'aggregate.meta'
    parse(file)


if __name__ == '__main__':
    main()
