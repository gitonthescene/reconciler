import pandas as pd
import json
from reconciler.webutils import get_query_dict, perform_query
import pytest

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal", "FAKE_CITY_HERE"],
    }
)
input_keys, reformatted = get_query_dict(test_df["City"], qid_type="Q515")


def test_get_query_dict():

    expected = {
        0: {"query": "Rio de Janeiro", "type": "Q515"},
        1: {"query": "São Paulo", "type": "Q515"},
        2: {"query": "Natal", "type": "Q515"},
        3: {"query": "FAKE_CITY_HERE", "type": "Q515"},
    }

    assert expected == reformatted


def test_perform_query():

    query_string = json.dumps({"queries": json.dumps(reformatted)})
    query_res = perform_query(query_string)

    assert len(query_res.keys()) == 4