import os
import json
import pytest
from app.api.parser import Parse

def test_pkg_data():
    sample_file = 'tests/sample1.meta'

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

    pkg2 = result["[0xxon/zeek-network-statistics]"]




