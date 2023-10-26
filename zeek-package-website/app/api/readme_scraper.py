import re
import os
import json


fields = {"test_cmd": "test command", "build_cmd": "build command",
          "depends": "dependencies"}


def load_packages() -> []:
    filepath = f"{os.getcwd()}/../json_files"

    for filename in os.listdir(filepath):
        if ".json" in filename:
            package_json = None
            changes = 0
            with open(f"{filepath}/{filename}", "r", encoding="utf-8") as file:
                package_json = json.load(file)
                if package_json["readme"] is not None:
                    missing = find_missing(package_json)
                    for field in missing:
                        item = get_field(package_json["readme"], field)
                        if item is not None:
                            package_json[field] = item
                            changes += 1

            if changes > 0:
                with open(f"{filepath}/{filename}",
                          "w+", encoding="utf-8") as file:
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

