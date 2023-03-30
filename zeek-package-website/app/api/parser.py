import re


class Parse:
    def __init__(self, file):
        with open(file, 'r') as f:
            contents = f.read()

        section_headers = self.find_section_headers(contents)
        descriptions = self.find_descriptions(contents)

        # Combine section headers and descriptions into tuples
        #self.results = list(zip(section_headers, descriptions))

    def find_section_headers(self, file_contents):
        section_headers = re.findall(
            r'\[[^/^][^[]*?\/[^[]*?\]',
            file_contents,
            flags=re.DOTALL)
        return section_headers

    def find_descriptions(self, file_contents):
        matches = re.findall(
            r'\[[^/^][^[]*?\/[^[]*?\][^[]*',
            file_contents,
            flags=re.DOTALL)
        
        # empty list of descs to append
        descriptions = []

        for match in matches:
            description_match = re.search(
                r'^description\s*=\s*(.+)', match, flags=re.MULTILINE)
            if description_match:
                description = description_match.group(1)
                descriptions.append(description)
        return descriptions


def main():
    file = 'aggregate.meta'
    parse = Parse(file)

    package_num = 1

    for section_header, description in parse.results:
        print(f"Package {package_num}:")
        print(section_header)
        print(description)
        print()

        package_num += 1


if __name__ == '__main__':
    main()
