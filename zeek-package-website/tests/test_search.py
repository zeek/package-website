import sys
import os
import pytest
import pickle
from app.api.search import search as s


class TestRank:

    query = "http"
    documents = []
    project_dir = os.path.dirname(os.path.abspath(__file__))
    json_files_dir = os.path.join(project_dir, "app/api/search/json_files")
    document_names = os.listdir(json_files_dir)
    for name in document_names:
        text_file = open(os.path.join(json_files_dir, name), "r")
        data = text_file.read()
        data = data.split("readme")[1]
        data = data.lower().split()
        documents.append(data)
        text_file.close()

    file = open("tests/http_rankings", "rb")
    saved_rankings = pickle.load(file)
    file.close()
    rankings = s.rank(documents, query)

    def test_rank_none(self):
        with pytest.raises(TypeError):
            s.rank(None, self.query)

    def test_rank_correct(self):
        assert self.rankings == self.saved_rankings

    def test_rank_type(self):
        print(type(self.rankings))
        assert str(type(self.rankings)) == "<class 'list'>"


class TestBias:

    input_dict = {"hello.json": 0, "hello.git": 0, "hello": 0}

    def test_bias_correct_json(self):
        desired = [('hello.json', 0), ('hello.git', 0), ('hello', 0)]

        output = s.bias(self.input_dict, "json")

        assert output == desired

    def test_bias_correct_git(self):

        desired = [('hello.json', 0), ('hello.git', 0), ('hello', 0)]

        output = s.bias(self.input_dict, "git")

        assert output == desired

    def test_bias_correct(self):

        desired = [('hello.json', 3), ('hello.git', 3), ('hello', 3)]

        output = s.bias(self.input_dict, "hello")

        assert output == desired

    def test_bias_none_rankings(self):

        assert s.bias(None, "hello") is None

    def test_bias_none_query(self):

        assert s.bias(self.input_dict, None) is None


class TestCutoff:

    input_list = [('hello.json', 3.12), ('hello.git', 0.22), ('hello', -.2)]

    def test_cutoff_correct(self):

        desired = self.input_list[:-1]

        output = s.get_lower_bound(self.input_list)

        assert desired == self.input_list[0:output]

    def test_cutoff_none(self):

        assert s.get_lower_bound(None) is None
