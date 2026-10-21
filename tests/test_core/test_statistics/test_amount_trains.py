"""This module test the module that computs from given departure and arrival stations, 
the amount of delayed at departure and arrival, and cancelled trains. Over each month, 
the ratio is computed from the amount of delayed/cancelled trains over the total planned
trains on a given period."""

import pandas as pd
from core.statistics import amount_trains as am
import pytest
import numpy as np
from core import load_data as ld
        
ld.init()

def test_get_total_cancelled_trains() -> None:
    result = am.get_total_cancelled_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], ld.df)
    assert result == 703
    
    result = am.get_total_cancelled_trains("BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12,
                                           [2019], ld.df)
    assert np.isnan(result)

def test_get_total_planned_trains() -> None:
    result = am.get_total_planned_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], ld.df)
    
    assert result == 7110
    
    result = am.get_total_planned_trains("BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12,
                                           [2019], ld.df)
    assert np.isnan(result)

def test_get_total_delayed_departure_trains() -> None:
    result = am.get_total_delayed_departure_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], ld.df)
    
    assert result == 1252
    
    result = am.get_total_delayed_departure_trains("BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12,
                                           [2019], ld.df)
    assert np.isnan(result)
    
def test_get_total_delayed_arrival_trains() -> None:
    result = am.get_total_delayed_arrival_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], ld.df)
    
    assert result == 905
    
    result = am.get_total_delayed_arrival_trains("BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12,
                                           [2019], ld.df)
    assert np.isnan(result)