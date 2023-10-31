"""
Parser utility for scraping values from aggragate.meta
"""
import re
import requests
import json
import os

class Parse(object):
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
        self.readme = None          # readmes
        self.pkg_dict = {}          # store the packages as a dict

    def parse_data(self) -> dict:
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

        # empty dict
        self.pkg_dict = {}

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
            self.get_next("depends", header)
            self.test_cmd = self.get_line("test_command", header)
            self.build_cmd = self.get_line("build_command", header)
            self.url = self.get_line("url", header)
            self.summary = self.get_line("summary", header)
            self.script_dir = self.get_line("script_dir", header)
            self.plugin_dir = self.get_line("plugin_dir", header)
            self.readme = self.get_readme()
            if self.readme is not None and self.url is not None:
                self.get_images()

            self.pkg_dict[self.section_header] = {
                "description": self.description,
                "tags": self.tags,
                "version": self.version,
                "depends": self.depends,
                "test_cmd": self.test_cmd,
                "build_cmd": self.build_cmd,
                "url": self.url,
                "summary": self.summary,
                "script_dir": self.script_dir,
                "plugin_dir": self.plugin_dir,
                "readme": self.readme
            }


            # section_count to keep track of # of packages
            self.section_count += 1

        return self.pkg_dict



    def get_name(self) -> str:
        """
        @brief Finds all section headers in the file contents.
        search and return all TOML styled section headers enclosed in
        brackets [ ]
        @param self: A reference to the current object.
        @return: section headers found in the file contents as strings.
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
        same_match = re.search(
            rf'^{text}\s*=\s*(.+)',
            header,
            flags=re.MULTILINE)

        if same_match:
            same_line = same_match.group(1)
        else:
            same_line = None

        return same_line

    def get_next(self, text, header) -> list:
        """
        @brief Extracts package dependencies
        @param self: A reference to the current object.
        @param header: The section header to search for the tags field.
        @return The list of dependencies, or None if not found.
        """
        next_match = re.search(
            rf'^{text}\s*=\s*(.*(?:\n\s+.*)*)',
            header,
            flags=re.MULTILINE)

        if next_match:
            next_line = next_match.group(1).strip().split('\n')
            # remove tabs
            next_line = [ln.replace('\t', '') for ln in next_line]
        else:
            next_line = None

        return next_line

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
            print(f"Has Readme = {self.readme is not None}")
            print()

    def dump(self):

        for item in self.pkg_dict.items():
            name = item[0].split("/")[1]
            name = name.strip("]")
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_files_dir = os.path.join(project_dir, "api", "search", "json_files")
            with open(f"{json_files_dir}/{name}.json", "w+",
                      encoding="utf-8") as outfile:
                outfile.write(json.dumps(item[1]))


    def get_readme(self) -> str:
        """
        @brief Use HTTP requests to find readme's for packages
        @param self: a reference to the current object
        @return: The readme obtained from the http request or None if not found
        """
        if self.url is not None:
            name = self.url
            name = name.removeprefix("https://github.com/")
            name = name.rstrip("/")
        else:
            name = self.section_header
            name = name.strip("[]")

        name = name.removesuffix(".git")
        request_url = f"https://raw.githubusercontent.com/{name}/master"

        # if packages have other forms of readme add to this list
        filenames = ["README.md", "readme.md", "README", "readme", "Readme.md",
                     "Readme", "README.rst", "Readme.rst", "readme.rst"]
        counter = 1

        readme_ext = filenames[0]
        get_request = requests.get(f"{request_url}/{readme_ext}")

        while not get_request.ok and counter < len(filenames):
            readme_ext = filenames[counter]
            get_request = requests.get(f"{request_url}/{readme_ext}")
            print(f"{request_url}/{readme_ext}")
            counter += 1

        # check for special case, as one package uses gitlab
        if "https://gitlab.com" in name:
            get_request = requests.get(f"{name}/-/raw/master/README.md")

        if not get_request.ok:
            return None

        return get_request.content.decode("utf-8")

    def get_images(self):
        url = self.url
        readme = self.readme

        url = url.replace(".git", "")
        url = url.replace("https://github.com",
                          "https://raw.githubusercontent.com")

        if url[-1] != "/":
            url += "/"

        url += "master/"

        readme = readme.replace('src="', f'src="{url}')

        readme = readme.split("(")

        for i in range(0, len(readme)-1):
            if(readme[i].endswith("]") and not readme[i+1].startswith("https://")):
                readme[i+1] = ''.join([url, readme[i+1]])

        readme = "(".join(readme)

        self.readme = readme


def main():
    file = 'aggregate.meta'
    # parse the file for all of its fields
    parser = Parse(file)
    # print the parsed data
    #parser.print_data()
    parser.parse_data()
    parser.dump()

    # Access the pkg_dict dictionary to print the extracted package data
    """
    for section_header, package_data in parser.pkg_dict.items():
        print(f"Package name: {section_header}")
        print(f"\tDescription: {package_data['description']}")
        print(f"\tTags: {package_data['tags']}")
        print(f"\tVersion: {package_data['version']}")
        print(f"\tDepends: {package_data['depends']}")
        print(f"\tTest command: {package_data['test_cmd']}")
        print(f"\tBuild command: {package_data['build_cmd']}")
        print(f"\tURL: {package_data['url']}")
        print(f"\tSummary: {package_data['summary']}")
        print(f"\tScript dir: {package_data['script_dir']}")
        print(f"\tPlugin dir: {package_data['plugin_dir']}")
        #print(f"\tReadme: {package_data['readme']}")
    """

    # get a specific package NOTE: be sure to include outside brackets
    #pkg = parser.pkg_dict["[corelight/callstranger-detector]"]
    #print(pkg)

    # print all packages as dicts
    for key, val, in parser.pkg_dict.items():
        print(key, val)




if __name__ == '__main__':
    main()
