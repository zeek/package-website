import os
import json
import pytest
from app.api.parser import Parse

sample_file = 'tests/sample1.meta'

def test_pkg_data_a():
    '''
    Some simple assertions 
    '''
    parser = Parse(sample_file)
    result = parser.parse_data()

    # test package from sample1.meta
    pkg1 = parser.pkg_dict["[0xxon/cve-2020-13777]"]

    assert pkg1["description"] == '"Test script for CVE-2020-13777. Please read Readme."'
    assert pkg1["tags"] is None
    assert pkg1["version"] == "main"
    #print(pkg1)
    #print(pkg1["depends"])
    assert pkg1["depends"] == ['zkg >=2.0', 'zeek >=4.0.0']
    assert pkg1["test_cmd"] == "cd testing && btest -d"
    assert pkg1["url"] == "https://github.com/0xxon/cve-2020-13777"
    assert pkg1["script_dir"] == "scripts"
    assert pkg1["plugin_dir"] is None

def test_pkg_data_b():
    parser = Parse(sample_file)
    result = parser.parse_data()

    pkg2 = result["[0xxon/zeek-network-statistics]"]
    assert pkg2["description"] == "Perform regular network measurements and report results."
    assert pkg2["tags"] == "topk, sumstats"
    assert pkg2["version"] == "main"
    assert pkg2["depends"] is None
    assert pkg2["test_cmd"] == "cd tests && make"
    assert pkg2["url"] == "https://github.com/0xxon/zeek-network-statistics"
    assert pkg2["script_dir"] == "scripts"
    assert pkg2["plugin_dir"] is None

def test_get_line():
    parser = Parse(sample_file)

    # test get current line
    header = "[0xxon/cve-2020-13777]\ncredits = Open Source Community"
    result = parser.get_line("credits", header)
    assert result == "Open Source Community"

    header = "[0xxon/cve-2020-13777]\ndescription = Test Description"
    result = parser.get_line("description", header)
    assert result == "Test Description"


def test_get_next():
    parser = Parse(sample_file)

    # test get next line
    header = "[0xxon/cve-2020-13777]\ndepends =\n    zkg >=2.0\n    zeek >=4.0.0"
    result = parser.get_next("depends", header)
    assert result == ["zkg >=2.0", "zeek >=4.0.0"]


