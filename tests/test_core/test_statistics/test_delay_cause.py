import pytest
import pandas as pd
from unittest.mock import patch
from core.statistics.delay_cause import (
    get_mean_cause_list,
    get_mean_of_external_cause,
    get_mean_of_infrastructural_cause,
    get_mean_of_traffic_management_cause,
    get_mean_of_mobile_equipment_cause,
    get_mean_of_railstation_management_cause,
    get_mean_of_traveler_cause,
    get_mean_of_unknown_cause,
)
import core.load_data as ld


@pytest.fixture
def mock_df():
    """Provides a mock DataFrame with delay causes for testing"""
    data = {
        ld.DEPARTURE_STATION_KEY: ["Paris", "Paris", "Lyon", "Marseille"],
        ld.ARRIVAL_STATION_KEY: ["Lyon", "Marseille", "Paris", "Paris"],
        ld.MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT: [10.0, 20.0, 30.0, 40.0],
        ld.MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT: [5.0, 15.0, 25.0, 35.0],
        ld.MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT: [2.0, 12.0, 22.0, 32.0],
        ld.MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT: [1.0, 11.0, 21.0, 31.0],
        ld.MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT: [0.0, 10.0, 20.0, 30.0],
        ld.MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT: [100.0, 200.0, 300.0, 400.0],
        ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT: [50.0, 150.0, 250.0, 350.0],
    }
    return pd.DataFrame(data)


@pytest.fixture(autouse=True)
def setup_mock_df(mock_df):
    """Patches the global df in load_data module before each test"""
    with patch("core.load_data.df", mock_df, create=True):
        yield


def test_get_mean_of_external_cause():
    # Global mean: (10+20+30+40)/4 = 25.0
    assert get_mean_of_external_cause() == 25.0
    # Paris -> Lyon: 10.0
    assert get_mean_of_external_cause("Paris", "Lyon") == 10.0
    # Paris -> Marseille: 20.0
    assert get_mean_of_external_cause("Paris", "Marseille") == 20.0


def test_get_mean_of_infrastructural_cause():
    # Global mean: (5+15+25+35)/4 = 20.0
    assert get_mean_of_infrastructural_cause() == 20.0
    # Paris -> Lyon: 5.0
    assert get_mean_of_infrastructural_cause("Paris", "Lyon") == 5.0


def test_get_mean_of_traffic_management_cause():
    # Global mean: (2+12+22+32)/4 = 17.0
    assert get_mean_of_traffic_management_cause() == 17.0
    # Lyon -> Paris: 22.0
    assert get_mean_of_traffic_management_cause("Lyon", "Paris") == 22.0


def test_get_mean_of_mobile_equipment_cause():
    # Global mean: (1+11+21+31)/4 = 16.0
    assert get_mean_of_mobile_equipment_cause() == 16.0
    # Marseille -> Paris: 31.0
    assert get_mean_of_mobile_equipment_cause("Marseille", "Paris") == 31.0


def test_get_mean_of_railstation_management_cause():
    # Global mean: (0+10+20+30)/4 = 15.0
    assert get_mean_of_railstation_management_cause() == 15.0
    # Paris -> Marseille: 10.0
    assert get_mean_of_railstation_management_cause("Paris", "Marseille") == 10.0


def test_get_mean_of_traveler_cause():
    # Global mean: (100+200+300+400)/4 = 250.0
    assert get_mean_of_traveler_cause() == 250.0
    # Lyon -> Paris: 300.0
    assert get_mean_of_traveler_cause("Lyon", "Paris") == 300.0


def test_get_mean_of_unknown_cause():
    # Global mean: (50+150+250+350)/4 = 200.0
    assert get_mean_of_unknown_cause() == 200.0
    # Marseille -> Paris: 350.0
    assert get_mean_of_unknown_cause("Marseille", "Paris") == 350.0


def test_get_mean_cause_list():
    """
    Tests that get_mean_cause_list returns a list containing the mean of all 7 causes.
    """
    result = get_mean_cause_list()
    assert len(result) == 7
    # Verify one of them (external cause)
    assert result[0] == get_mean_of_external_cause()
    # Verify all are floats
    assert all(isinstance(x, float) for x in result)


def test_get_mean_cause_list_filtered():
    """
    Tests get_mean_cause_list with filters.
    """
    result = get_mean_cause_list("Paris", "Lyon")
    assert len(result) == 7
    assert result[0] == 10.0  # external
    assert result[1] == 5.0  # infrastructural
    assert result[2] == 2.0  # traffic
    assert result[3] == 1.0  # mobile
    assert result[4] == 0.0  # railstation
    assert result[5] == 100.0  # traveler
    assert result[6] == 50.0  # unknown
