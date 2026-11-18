import numpy as np
import pandas as pd

from core.statistics import mean_delay as md


def test_weighted_mean_delay_mixed_data() -> None:
    """Test that the function calculates the weighted mean delay
    with both valid and invalid observations mixed together"""

    monthly_planned_trains = pd.Series([100, 300, 0, -5, np.nan, 200])
    delay_observations = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0, np.nan])

    result = md.weighted_mean_delay(
        monthly_planned_trains,
        delay_observations,
    )

    # check the weighted mean for the valid observations
    assert result == 17.5


def test_weighted_mean_delay_without_valid_data() -> None:
    """Test the weighted mean delay when there is no valid observation"""

    monthly_planned_trains = pd.Series([0, -5, np.nan, 100])
    delay_observations = pd.Series([10.0, 20.0, 30.0, np.nan])

    result = md.weighted_mean_delay(
        monthly_planned_trains,
        delay_observations,
    )

    # check the result is NaN
    assert pd.isna(result)
