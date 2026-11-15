import numpy as np
import pytest

from core.statistics import delay_seasonal_distribution as dsd


def test_delay_distribution_with_two_observations(mocked_delay_df) -> None:
    """Test a selection of the statistics
    calculated with 2 observations :
    the minimum, the median and the maximum"""

    result = dsd.calculate_mean_arrival_delay_distribution_per_month(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        [2022, 2023],
        mocked_delay_df,
    )

    # check the distribution statistics (selection)
    assert result["minimum"] == 30.0
    assert result["median"] == 35.0
    assert result["maximum"] == 40.0

    # check the number of previous years' observations and delayed trains
    assert result["number_historical_year_observations"] == 2
    assert result["sum_arr_delayed_trains"] == 220

    # the function should not calculat quartiles
    # with only 2 observations
    assert np.isnan(result["q1"])
    assert np.isnan(result["q3"])


def test_delay_distribution_with_five_observations(mocked_delay_df) -> None:
    """Test the calculation of all statistics with 5 observations."""

    result = dsd.calculate_mean_arrival_delay_distribution_per_month(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        [2018, 2019, 2020, 2022, 2023],
        mocked_delay_df,
    )

    # check the distribution statistics
    assert result["minimum"] == pytest.approx(20.1)
    assert result["q1"] == pytest.approx(21.10280374)
    assert result["median"] == pytest.approx(22.5)
    assert result["q3"] == pytest.approx(30.0)
    assert result["maximum"] == pytest.approx(40.0)

    # check the number of previous years' observations and delayed trains
    assert result["number_historical_year_observations"] == 5
    assert result["sum_arr_delayed_trains"] == 542


def test_delay_distribution_with_no_observations(mocked_delay_df) -> None:
    """Test the result when no observations are available.
    The function should return NaN for the 5 statistics,
    return 0 for the number of previous years' observations,
    and None for the sum of delayed trains at arrival"""

    result = dsd.calculate_mean_arrival_delay_distribution_per_month(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        [2017],
        mocked_delay_df,
    )

    # check the distribution statistics
    assert np.isnan(result["minimum"])
    assert np.isnan(result["q1"])
    assert np.isnan(result["median"])
    assert np.isnan(result["q3"])
    assert np.isnan(result["maximum"])

    # check the number of previous years' observations and delayed trains
    assert result["number_historical_year_observations"] == 0
    assert result["sum_arr_delayed_trains"] is None


def test_delay_distribution_with_one_observation(mocked_delay_df) -> None:
    """Test that only the median is calculated if there is 1 observation."""

    result = dsd.calculate_mean_arrival_delay_distribution_per_month(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        [2019],
        mocked_delay_df,
    )

    assert result["median"] == pytest.approx(20.1)

    assert np.isnan(result["minimum"])
    assert np.isnan(result["q1"])
    assert np.isnan(result["q3"])
    assert np.isnan(result["maximum"])

    # check the number of observations and delayed trains
    assert result["number_historical_year_observations"] == 1
    assert result["sum_arr_delayed_trains"] == 96


def test_delay_distribution_with_missing_train_count(mocked_delay_df) -> None:
    """Test the result when the number of delayed trains is missing."""

    result = dsd.calculate_mean_arrival_delay_distribution_per_month(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        [2022, 2024],
        mocked_delay_df,
    )

    # check the distribution statistics
    assert result["minimum"] == 30.0
    assert result["median"] == 40.0
    assert result["maximum"] == 50.0

    # check the number of previous years' observations and delayed trains
    assert result["number_historical_year_observations"] == 2
    assert result["sum_arr_delayed_trains"] is None


def test_generate_historical_monthly_mean_arrival_delay_distribution_dataframe(
    mocked_delay_df,
) -> None:
    """Test the generation of previous years' statistics for different months
    with different numbers of observations."""

    result = dsd.generate_historical_monthly_mean_arrival_delay_distribution_dataframe(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        3,
        [2019, 2022, 2023],
        mocked_delay_df,
    )

    # check the number of months and the order
    assert len(result) == 3
    assert result["month"].tolist() == [1, 2, 3]

    # January with 3 observations
    assert result.loc[0, "median"] == pytest.approx(30.0)
    assert result.loc[0, "number_historical_year_observations"] == 3
    assert result.loc[0, "sum_arr_delayed_trains"] == 316

    # February with 1 observation
    assert result.loc[1, "median"] == pytest.approx(26.3)
    assert result.loc[1, "number_historical_year_observations"] == 1

    # March with no observation
    assert np.isnan(result.loc[2, "median"])
    assert result.loc[2, "number_historical_year_observations"] == 0


def test_get_monthly_mean_arrival_delay_global_dataframe(mocked_delay_df) -> None:
    """Test the generation of the dataframe combining the previous years' statistics
    and the current year (2026) observations."""

    selected_years = [2019, 2022, 2023, 2026]

    result = dsd.get_monthly_mean_arrival_delay_global_dataframe(
        "PARIS MONTPARNASSE",
        "RENNES",
        1,
        2,
        selected_years,
        mocked_delay_df,
        actual_year=2026,
    )

    # check the months
    assert len(result) == 2
    assert result["month"].tolist() == [1, 2]

    # check January
    assert result.loc[0, "median"] == pytest.approx(30.0)
    assert result.loc[0, "number_historical_year_observations"] == 3
    assert result.loc[0, "mean_arrival_delay_actual_year"] == 35.0
    assert result.loc[0, "number_arr_delayed_trains_actual_year"] == 110

    # check February 2026 with no observations
    assert np.isnan(result.loc[1, "mean_arrival_delay_actual_year"])

    # check that the original list of years has not been modified
    # the function should work only with the .copy
    assert selected_years == [2019, 2022, 2023, 2026]
