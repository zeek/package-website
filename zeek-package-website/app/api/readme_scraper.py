import re
import os
import json


fields = {"test_cmd": "test command", "build_cmd": "build command",
          "depends": "dependencies"}


def load_packages() -> []:
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(project_dir, "search", "json_files")
    print("loading")
    for filename in os.listdir(filepath):
        if ".json" in filename:
            package_json = None
            with open(f"{filepath}/{filename}", "r", encoding="utf-8") as file:
                package_json = json.load(file)
                if package_json["readme"] is not None:
                    missing = find_missing(package_json)
                    for field in missing:
                        item = get_field(package_json["readme"], field)
                        if item is not None:
                            package_json[field] = item
                    package_json["readme"] = get_images(package_json["readme"],
                                                        package_json["url"])

            with open(f"{filepath}/{filename}", "w+",
                      encoding="utf-8") as file:
                json.dump(package_json, file)


def find_missing(package: dict) -> []:
    missing = []

    for key in package.keys():
        if package[key] is None and key in fields.keys():
            missing.append(key)

    return missing


def get_field(readme: str, field: str) -> str:

    search_term = f"{fields[field]}"

    field = re.search(f'(?<=# {search_term})(.*)(?=\n)', readme.lower())
    term = None

    if field is not None:
        term = re.search(r'(?<=`)(.*)(?=`)', field.group())

        if term is not None:
            return term.group()

        return field.group()

    return None


def get_images(readme, url):
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

    return readme
