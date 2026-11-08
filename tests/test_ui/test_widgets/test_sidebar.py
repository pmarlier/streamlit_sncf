import numpy as np
import pytest
import streamlit as st

from ui.widgets import sidebar


def test_get_month_from_int_str():
    """Test conversion of month integer to string."""
    assert sidebar.get_month_from_int_str(1) == "Janvier"
    assert sidebar.get_month_from_int_str(12) == "Décembre"
    with pytest.raises(KeyError):
        sidebar.get_month_from_int_str(13)


def test_get_month_from_str_int():
    """Test conversion of month string to integer."""
    assert sidebar.get_month_from_str_int("Janvier") == 1
    assert sidebar.get_month_from_str_int("Décembre") == 12
    with pytest.raises(KeyError):
        sidebar.get_month_from_str_int("Unknown")
