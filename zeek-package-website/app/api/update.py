#!/usr/bin/env python3

import subprocess
from app.api.parser import Parse
from app.api.readme_scraper import load_packages
import os


def update(file: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    std_out = subprocess.run(
        ["git", "-C", dir_path, "pull", "origin", "main"], capture_output=True
    ).stdout.decode("utf-8")

    if "Already up to date.\n" not in std_out:
        print("Parsing")
        parse = Parse(f"{dir_path}/{file}")
        parse.parse_data()
        parse.dump()
        load_packages()
        print("Parsed")
    else:
        print(std_out)


def main():
    update("aggregate.meta")


if __name__ == "__main__":
    main()
