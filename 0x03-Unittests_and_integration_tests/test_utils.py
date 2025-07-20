#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from utils import get_json
from parameterized import parameterized
from typing import Mapping, Dict, Sequence, Any


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])

    def test_access_nested_map(self, input:Mapping[str, int], path:Sequence, expected):
        self.assertEqual(access_nested_map(input, path), expected)

    @parameterized.expand([({}, ("a"), KeyError), ({"a":1}, ("a", "b"), KeyError)])

    def test_access_nested_map_exception(self, input:Mapping, path:Sequence, expected):
        self.assertRaises(KeyError, access_nested_map, input, path)

class TestGetJson(unittest.TestCase):
        
    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, name, url, expected, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response
        response = get_json(url)
        self.assertEqual(response, expected)
        mock_get.assert_called_once_with(url)

