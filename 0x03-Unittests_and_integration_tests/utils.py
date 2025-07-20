#!/usr/bin/envpython3
import requests
from typing import Dict

def get_json(url: str) -> Dict:
    """Get JSON from remote URL"""
    response = requests.get(url)
    return response.json()
