"""This module test the module that computs from given departure and arrival stations,
the amount of delayed at departure and arrival, and cancelled trains. Over each month,
the ratio is computed from the amount of delayed/cancelled trains over the total planned
trains on a given period."""

import numpy as np
import pandas as pd
import pytest

from core import load_data as ld
from core.statistics import amount_trains as am


def test_get_ratio_cancelled_trains(mocked_df) -> None:
    # initialize load_data module with real dataframe to cover initial test case
    ld.init()
    # call method with no dataframe and check only if a result is given
    # based on real data, so limit test to result type check
    result = am.get_ratio_cancelled_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018], None
    )
    assert isinstance(result, float)

    # initialize load_data module with mocked dataframe to check computation
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = am.get_ratio_cancelled_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018], ld.df
    )
    assert result == pytest.approx(50 / 1736)

    result = am.get_ratio_cancelled_trains(
        "RENNES", "PARIS MONTPARNASSE", 1, 12, [2018], ld.df
    )
    assert result == pytest.approx(4 / 599)


def test_get_total_planned_trains(mocked_df) -> None:
    # initialize load_data module with real dataframe to cover initial test case
    ld.init()
    # call method with no dataframe and check only if a result is given
    # based on real data, so limit test to result type check
    result = am.get_total_planned_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018], None
    )
    assert isinstance(result, float)

    # initialize load_data module with mocked dataframe to check computation
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = am.get_total_planned_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018, 2020], ld.df
    )
    assert result == 2346

    result = am.get_total_planned_trains(
        "BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12, [2019], ld.df
    )
    assert np.isnan(result)


def test_get_ratio_delayed_departure_trains(mocked_df) -> None:
    # initialize load_data module with real dataframe to cover initial test case
    ld.init()
    # call method with no dataframe and check only if a result is given
    # based on real data, so limit test to result type check
    result = am.get_ratio_delayed_departure_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018], None
    )
    assert isinstance(result, float)

    # initialize load_data module with mocked dataframe to check computation
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = am.get_ratio_delayed_departure_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018, 2020], ld.df
    )
    assert result == pytest.approx(379 / 2346)

    result = am.get_ratio_delayed_departure_trains(
        "BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12, [2019], ld.df
    )
    assert np.isnan(result)


def test_get_ratio_delayed_arrival_trains(mocked_df) -> None:
    # initialize load_data module with real dataframe to cover initial test case
    ld.init()
    # call method with no dataframe and check only if a result is given
    # based on real data, so limit test to result type check
    result = am.get_ratio_delayed_arrival_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018], None
    )
    assert isinstance(result, float)

    # initialize load_data module with mocked dataframe to check computation
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = am.get_ratio_delayed_arrival_trains(
        "PARIS MONTPARNASSE", "RENNES", 1, 12, [2018, 2020], ld.df
    )

    assert result == pytest.approx(456 / 2346)

    result = am.get_ratio_delayed_arrival_trains(
        "BORDEAUX ST JEAN", "PARIS VAUGIRARD", 2, 12, [2019], ld.df
    )
    assert np.isnan(result)
