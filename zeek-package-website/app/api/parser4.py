import re

def find_headers(contents):
    headers = re.findall(
        r'\[[^/^][^[]*?\/[^[]*?\][^[]*',
        contents,
        flags=re.DOTALL)
    return headers

def find_description(header):
    description_match = re.search(
        r'^description\s*=\s*(.+)', header, flags=re.MULTILINE)
    if description_match:
        description = description_match.group(1)
    else:
        description = None
    return description

def parse(file):
    with open(file, 'r') as f:
        contents = f.read()

    # Find all section headers in the file contents
    headers = find_headers(contents)

    # Initialize a counter for the section headers
    section_count = 1

    # Loop over each header and extract the desired fields
    for header in headers:
        # Extract the section header
        section_header = re.search(r'\[[^/^].*?\/[^[]*?\]', header).group(0)

        # Extract the description
        description = find_description(header)

        # Print the section number, header, and description
        print(f"Section {section_count}: {section_header}")
        if description:
            print(description)
        print()  # Print a blank line between entries

        # Increment the section count
        section_count += 1

def main():
    file = 'aggregate.meta'
    parse(file)

if __name__ == '__main__':
    main()

