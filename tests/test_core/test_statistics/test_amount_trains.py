"""This module test the module that computs from given departure and arrival stations, 
the amount of delayed at departure and arrival, and cancelled trains. Over each month, 
the ratio is computed from the amount of delayed/cancelled trains over the total planned
trains on a given period."""

import pandas as pd
from core.statistics import amount_trains as am
import pytest

def test_get_total_cancelled_trains(mocked_df: pd.DataFrame) -> None:
    result = am.get_total_cancelled_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], mocked_df)
    
    assert result == 49

def test_get_total_planned_trains(mocked_df: pd.DataFrame) -> None:
    result = am.get_total_planned_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], mocked_df)
    
    assert result == 1146

def test_get_total_delayed_departure_trains(mocked_df: pd.DataFrame) -> None:
    result = am.get_total_delayed_departure_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], mocked_df)
    
    assert result == 202
    
def test_get_total_delayed_arrival_trains(mocked_df: pd.DataFrame) -> None:
    result = am.get_total_delayed_arrival_trains("PARIS MONTPARNASSE", "RENNES", 2, 12, 
                                           [2018, 2020], mocked_df)
    
    assert result == 230