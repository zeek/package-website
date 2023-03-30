"""
Parser utility for scraping values from aggragate.meta
"""
# TODO:
# * FIXME REGEX for descriptions... take into account data on the next
#       line. IF data is on the next line, it is suffixed with tabs
#
# * FIXME misc. key/val pairs that are not as common... look thru
#       aggragate.meta file pkg by pkg to see what is left to scrape
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
            self.author = self.get_author(header)
            self.description = self.get_desc(header)
            self.tags = self.get_tags(header)
            self.version = self.get_version(header)
            self.depends = self.get_depends(header)
            self.test_cmd = self.get_test_cmd(header)
            self.build_cmd = self.get_build_cmd(header)
            self.url = self.get_url(header)
            self.summary = self.get_summary(header)
            self.script_dir = self.get_script_dir(header)
            self.plugin_dir = self.get_plugin_dir(header)

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

    def get_author(self, header):
        """
        @brief Extracts the author/credits from a given section header.
        @param self: A reference to the current object.
        @param header: The section header to search for the author/credits field.
        @return: The author/credits value found in the header, or None if not found.
        """
        author_match = re.search(
            r'^credits\s*=\s*(.+)', header, flags=re.MULTILINE)
        if author_match:
            author = author_match.group(1)
        else:
            author = None
        return author

    def get_desc(self, header):
        """
        @brief Extracts the description from a given section header.
        @param self: A reference to the current object.
        @param header: The section header to search for the description field.
        @return: The description value found in the header, or None if not found.
        """
        description_match = re.search(
            r'^description\s*=\s*(.+)', header, flags=re.MULTILINE)
        if description_match:
            description = description_match.group(1)
        else:
            description = None
        return description

    def get_tags(self, header):
        """
        @brief Extracts the tags/pkg keywords from a given section header.
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return: The tags value found in the header, or None if not found.
        """
        tags_match = re.search(
            r'^tags\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if tags_match:
            tags = tags_match.group(1)
        else:
            tags = None
        return tags

    def get_version(self, header):
        """
        @brief Extracts the package version from the header string.
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The version value, or None if no version is found.
        """
        version_match = re.search(
            r'^version\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if version_match:
            version = version_match.group(1)
        else:
            version = None
        return version

    def get_depends(self, header):
        """
        @brief Extracts package dependencies
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The list of dependencies, or None if not found.
        """
        depends_match = re.search(
            r'^depends\s*=\s*(.*(?:\n\s+.*)*)',
            header,
            flags=re.MULTILINE)
        if depends_match:
            depends = depends_match.group(1).strip().split('\n')
            # remove tabs
            depends = [dep.replace('\t', '') for dep in depends]
        else:
            depends = None
        return depends

    def get_test_cmd(self, header):
        """
        @brief Extracts package test commands
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The list of test commands, or None if not found.
        """
        test_cmd_match = re.search(
            r'^test_command\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if test_cmd_match:
            test_cmd = test_cmd_match.group(1)
        else:
            test_cmd = None
        return test_cmd

    def get_build_cmd(self, header):
        """
        @brief Extracts package build commands
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The list of build commands, or None if not found.
        """
        build_cmd_match = re.search(
            r'^build_command\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if build_cmd_match:
            build_cmd = build_cmd_match.group(1)
        else:
            build_cmd = None
        return build_cmd

    def get_url(self, header):
        """
        @brief Extracts package repository URL
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The repo URL, or None if not found.
        """
        url_match = re.search(
            r'^url\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if url_match:
            url = url_match.group(1)
        else:
            url = None
        return url

    def get_summary(self, header):
        """
        @brief Extracts package summary
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The package summary, or None if not found.
        """
        summary_match = re.search(
            r'^summary\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if summary_match:
            summary = summary_match.group(1)
        else:
            summary = None
        return summary

    def get_script_dir(self, header):
        """
        @brief Extracts package script directory location
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The pkg script dir, or None if not found.
        """
        script_dir_match = re.search(
            r'^script_dir\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if script_dir_match:
            script_dir = script_dir_match.group(1)
        else:
            script_dir = None
        return script_dir

    def get_plugin_dir(self, header):
        """
        @brief Extracts package plugin directory location
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The pkg plugin dir, or None if not found.
        """
        plugin_dir_match = re.search(
            r'^plugin_dir\s*=\s*(.*)$', header, flags=re.MULTILINE)
        if plugin_dir_match:
            plugin_dir = plugin_dir_match.group(1)
        else:
            plugin_dir = None
        return plugin_dir

    def print_data(self):
        """
        @brief Prints the  parsed data.
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
