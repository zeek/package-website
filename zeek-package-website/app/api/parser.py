"""
Parser utility for scraping values from aggragate.meta
"""
# TODO:
# * FIXME REGEX for descriptions... take into account data on the next
#       line. IF data is on the next line, it is suffixed with tabs
#
# * FIXME misc. key/val pairs that are not as common... look thru
#       aggragate.meta file pkg by pkg to see what is left to scrape
#
# * FIXME move functions that use the same REGEX to a commmon
#       REGEX function. this will eliminate duplicated code

import re


class Parse:
    def __init__(self, file):
        """
        @brief Constructor for the Parse class. Sets needed values to
        parse to None
        @param file: The name of the file to be parsed.
        @return: None
        """
        with open(file, 'r') as f:
            self.contents = f.read()

        self.section_count = None   # number of packages
        self.section_header = None  # pkg names
        self.author = None          # pkg author/credits
        self.description = None     # pkg description
        self.tags = None            # pkg tags
        self.version = None         # pkg version
        self.depends = None         # pkg dependencies
        self.ext_depends = None     # pgk external dependencies
        self.test_cmd = None        # pkg test commands
        self.build_cmd = None       # pkg build commands
        self.url = None             # pkg repo URL
        self.summary = None         # pkg summary
        self.script_dir = None      # pkg script directory
        self.plugin_dir = None      # pkg plugin directory
        # TODO: implement REGEX method for this
        self.user_vars = None       # pkg user variables

    def parse_data(self):
        """
        @brief Extracts package information from the file contents.
        Loop over section headers and look for the specified key/value
        pairs located within. Yield the extracted data
        @param self: A reference to the current object.
        @return: A generator that yields the extracted fields for each package.
        """
        # find all package names
        headers = self.get_name()
        # initialize package counter
        self.section_count = 1

        # loop over each header and extract the desired fields
        for header in headers:
            # extract the section header
            self.section_header = re.search(
                r'\[[^/^].*?\/[^[]*?\]', header).group(0)
            # extract our desired fields
            # TODO: pass in header + text to look for
            self.author = self.get_line("credits", header)
            self.description = self.get_line("description", header)
            self.tags = self.get_line("tags", header)
            self.version = self.get_line("version", header)
            self.depends = self.get_next("depends", header)
            self.test_cmd = self.get_line("test_command", header)
            self.build_cmd = self.get_line("build_command", header)
            self.url = self.get_line("url", header)
            self.summary = self.get_line("summary", header)
            self.script_dir = self.get_line("script_dir", header)
            self.plugin_dir = self.get_line("plugin_dir", header)

            # yield the fields we retrieved
            yield (self.section_header,
                   self.description,
                   self.tags,
                   self.version,
                   self.depends,
                   self.test_cmd,
                   self.build_cmd,
                   self.url,
                   self.summary,
                   self.script_dir,
                   self.plugin_dir)
            # section_count to keep track of # of packages
            self.section_count += 1

    def get_name(self):
        """
        @brief Finds all section headers in the file contents.
        search and return all TOML styled section headers enclosed in
        brackets [ ]
        @param self: A reference to the current object.
        @return: A list of section headers found in the file contents.
        """
        headers = re.findall(
            r'\[[^/^][^[]*?\/[^[]*?\][^[]*',
            self.contents,
            flags=re.DOTALL)

        return headers

    def get_line(self, text, header) -> str:
        """
        @brief Extracts a specified text field from a given section header.
        Catches values on the same line after {text} =
        @param self: A reference to the current object.
        @param header: The section header to search for the author/credits field.
        @return: The author/credits value found in the header, or None if not found.
        """
        # generic regular expression
        reg = (r'^{text}\s*=\s*(.+)', text)
        regex_match = re.search(
            rf'^{text}\s*=\s*(.+)',
            header,
            flags=re.MULTILINE)

        if regex_match:
            same_line = regex_match.group(1)
        else:
            same_line = None

        return same_line

    def get_next(self, text, header):
        """
        @brief Extracts package dependencies
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The list of dependencies, or None if not found.
        """
        depends_match = re.search(
            rf'^{text}\s*=\s*(.*(?:\n\s+.*)*)',
            header,
            flags=re.MULTILINE)

        if depends_match:
            depends = depends_match.group(1).strip().split('\n')
            # remove tabs
            depends = [dep.replace('\t', '') for dep in depends]
        else:
            depends = None

        return depends

    def print_data(self):
        """
        @brief Print utility function for debugging.
        @param self: A reference to the current object.
        @return: None
        """
        for _ in self.parse_data():
            print(f"{self.section_count}: Name = {self.section_header}")
            print(f"Author = {self.author}")
            print(f"Description = {self.description}")
            print(f"Version = {self.version}")
            print(f"Tags = {self.tags}")
            print(f"Dependencies = {self.depends}")
            print(f"Test Command = {self.test_cmd}")
            print(f"Build Command = {self.build_cmd}")
            print(f"Repo URL = {self.url}")
            print(f"Summary = {self.summary}")
            print(f"Script Dir = {self.script_dir}")
            print(f"Plugin Dir = {self.plugin_dir}")
            print()


def main():
    file = 'aggregate.meta'
    # parse the file for all of its fields
    p = Parse(file)
    # print the parsed data
    p.print_data()


if __name__ == '__main__':
    main()
