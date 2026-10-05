
import json
import os
import pandas as pd
import pytest
from unidecode import unidecode
import sys

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(WORKING_DIR))

from core.railway_data import railway_geo as rg

def test_load_railway_geo_data():
    # testing default configuration with no filepath given as argument
    assert isinstance(rg.load_railstation_geo_data(), pd.DataFrame)
    with pytest.raises(FileNotFoundError) as exc_info:
        rg.load_railstation_geo_data("fake_path_for_exception_test")
        
#     <your code that should raise YourException>

# exception_raised = exc_info.value
# <do asserts here>
#     assert 