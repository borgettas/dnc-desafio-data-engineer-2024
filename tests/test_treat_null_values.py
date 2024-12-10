import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dags.commons.ingestion.normalization import treat_null_values_to_zero


def test_treat_null_values_to_zero():
    assert treat_null_values_to_zero(None) == 0
    assert treat_null_values_to_zero('') == 0
    assert treat_null_values_to_zero(' ') == 0

    assert treat_null_values_to_zero(1) == 1
    assert treat_null_values_to_zero('texto') == 'texto'
    assert treat_null_values_to_zero(0) == 0 
    assert treat_null_values_to_zero([]) == []
    assert treat_null_values_to_zero({}) == {}
