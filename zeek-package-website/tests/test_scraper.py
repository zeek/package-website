import sys
import os
import pytest
import json
from app.api import readme_scraper as s


class TestFindMissing:

    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(filepath, "tests")
    file = "sample.json"
    json_dict = None
    with open(f"{filepath}/{file}", "r", encoding="utf-8") as file:
        json_dict = json.load(file)

    def test_missing_correct(self):

        expected = ["depends", "test_cmd", "build_cmd"]
        actual = s.find_missing(self.json_dict)
        assert expected == actual

    def test_missing_none(self):

        assert s.find_missing(None) is None

class TestGetField:

    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(filepath, "tests")
    file = "sample.json"
    json_dict = None
    with open(f"{filepath}/{file}", "r", encoding="utf-8") as file:
        json_dict = json.load(file)
    readme = json_dict["readme"]
    field = "test_cmd"

    def test_field_correct(self):

        expected = "sample test command"
        result = s.get_field(self.readme, self.field)

        assert expected == result

    def test_field_none(self):

        assert s.get_field(None, None) is None
