import hashlib
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dags.commons.ingestion.hash import generate_hash


def test_generate_hash_with_string():
    assert generate_hash("test") == hashlib.sha256("test".encode()).hexdigest()

def test_generate_hash_with_integer():
    assert generate_hash(123) == hashlib.sha256("123".encode()).hexdigest()

def test_generate_hash_with_float():
    assert generate_hash(123.456) == hashlib.sha256("123.456".encode()).hexdigest()

def test_generate_hash_with_none():
    assert generate_hash(None) == hashlib.sha256("None".encode()).hexdigest()

def test_generate_hash_with_list():
    assert generate_hash([1, 2, 3]) == hashlib.sha256(str([1, 2, 3]).encode()).hexdigest()