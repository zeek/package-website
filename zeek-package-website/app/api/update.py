#!/usr/bin/env python3

import subprocess
from parser import Parse


def main():
    std_out = subprocess.run(["git", "pull", "origin", "main"],
                             capture_output=True).stdout
    file = 'aggregate.meta'

    if not std_out == b'Already up to date.\n':
        print("Parsing")
        parse = Parse(file)
        parse.parse_data()
        parse.dump
        print("Parsed")
    else:
        print(std_out.decode())


if __name__ == "__main__":
    main()
