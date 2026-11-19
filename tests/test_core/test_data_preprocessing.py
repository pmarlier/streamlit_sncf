import numpy as np
import pandas as pd
import pytest

from core.data_preprocessing import preprocess_data


def test_preprocess_covid_period(mocked_raw_sncf_df) -> None:
    """Test the invalidation of the data during the Covid period."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2019 : valid data
    assert result.loc[0, "Nombre de trains en retard à l'arrivée"] == 10
    assert result.loc[0, "Retard moyen des trains en retard à l'arrivée"] == 20.0

    # March 2020 : data invalidated
    assert np.isnan(result.loc[1, "Nombre de trains en retard à l'arrivée"])
    assert np.isnan(result.loc[1, "Retard moyen des trains en retard à l'arrivée"])

    # names of the station must be preserved
    assert result.loc[1, "Gare de départ"] == "PARIS MONTPARNASSE"
    assert result.loc[1, "Gare d'arrivée"] == "RENNES"


def test_preprocess_q1_2025(mocked_raw_sncf_df) -> None:
    """Test the invalidation of delays over 30 and 60 minutes in Q1 2025."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2019 : valid data
    assert result.loc[0, "Nombre trains en retard > 30min"] == 3
    assert result.loc[0, "Nombre trains en retard > 60min"] == 1

    # January 2025 :  data invalidated
    assert np.isnan(result.loc[2, "Nombre trains en retard > 30min"])
    assert np.isnan(result.loc[2, "Nombre trains en retard > 60min"])

    # other metrics remain valid
    assert result.loc[2, "Nombre trains en retard > 15min"] == 4
    assert result.loc[2, "Nombre de trains en retard à l'arrivée"] == 10


def test_preprocess_no_arrival_delay(mocked_raw_sncf_df) -> None:
    """Test the invalidation of average delay when no train is delayed."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2019 : valid average delay
    assert result.loc[0, "Retard moyen des trains en retard à l'arrivée"] == 20.0

    # January 2026 : no delayed trains
    assert result.loc[3, "Nombre de trains en retard à l'arrivée"] == 0
    assert np.isnan(result.loc[3, "Retard moyen des trains en retard à l'arrivée"])


def test_preprocess_no_departure_delay(mocked_raw_sncf_df) -> None:
    """Test the invalidation of average delay when no train is delayed at departure."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2019 : valid average departure delay
    assert result.loc[0, "Retard moyen des trains en retard au départ"] == 15.0

    # February 2026 : no delayed trains at departure
    assert result.loc[4, "Nombre de trains en retard au départ"] == 0
    assert np.isnan(result.loc[4, "Retard moyen des trains en retard au départ"])


def test_preprocess_imputation_with_historical_median(mocked_raw_sncf_df) -> None:
    """Test the imputation of invalid average delay using historical median."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2024: invalid average delay and replace it with historical median
    assert result.loc[5, "Retard moyen des trains en retard à l'arrivée"] == 25.0

    # valid historical observations remain unchanged
    assert result.loc[0, "Retard moyen des trains en retard à l'arrivée"] == 20.0
    assert result.loc[2, "Retard moyen des trains en retard à l'arrivée"] == 30.0


def test_preprocess_imputation_without_historical_data(mocked_raw_sncf_df) -> None:
    """Test the imputation when there is no valid historical data."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2024: is historical median correctly calculated ?
    assert result.loc[5, "Retard moyen des trains en retard à l'arrivée"] == 25.0

    # February 2026: invalid average delay without historical data
    assert np.isnan(result.loc[4, "Retard moyen des trains en retard à l'arrivée"])


def test_preprocess_unknown_delay_causes(mocked_raw_sncf_df) -> None:
    """Test the calculation of the percentage of unknown delay causes."""

    result = preprocess_data(mocked_raw_sncf_df)

    # January 2019: unknown causes represent 10%
    assert result.loc[0, "Prct retard causes non renseignées"] == 10.0

    # March 2020: Covid data invalidated
    assert np.isnan(result.loc[1, "Prct retard causes non renseignées"])

    # January 2026: no trains delayed at arrival
    assert np.isnan(result.loc[3, "Prct retard causes non renseignées"])


def test_preprocess_invalid_delays_over_15min(mocked_raw_sncf_df) -> None:
    """Test the invalidation of inconsistent delayed train counts over 15 minutes."""

    result = preprocess_data(mocked_raw_sncf_df)

    # March 2026: more trains delayed over 15 min than total delayed trains
    assert result.loc[6, "Nombre de trains en retard à l'arrivée"] == 10
    assert np.isnan(result.loc[6, "Nombre trains en retard > 15min"])

    # January 2019: check if valid delayed train count remains valid
    assert result.loc[0, "Nombre trains en retard > 15min"] == 4


def test_preprocess_negative_average_delays(mocked_raw_sncf_df) -> None:
    """Test the correction of negative average delays for all trains."""

    result = preprocess_data(mocked_raw_sncf_df)

    # check that positive average delays remain unchanged
    assert result.loc[0, "Retard moyen de tous les trains à l'arrivée"] == 3.0
    assert result.loc[0, "Retard moyen de tous les trains au départ"] == 2.0

    # check that zero values don't change
    assert result.loc[3, "Retard moyen de tous les trains à l'arrivée"] == 0.0
    assert result.loc[3, "Retard moyen de tous les trains au départ"] == 0.0

    # check that values between -1 and 0 are replaced by 0
    assert result.loc[4, "Retard moyen de tous les trains à l'arrivée"] == 0.0
    assert result.loc[5, "Retard moyen de tous les trains au départ"] == 0.0
    assert result.loc[5, "Retard moyen de tous les trains à l'arrivée"] == 0.0
    assert result.loc[6, "Retard moyen de tous les trains au départ"] == 0.0

    # check that values under the threshold (-1) are replaced by NaN
    assert np.isnan(result.loc[6, "Retard moyen de tous les trains à l'arrivée"])
    assert np.isnan(result.loc[4, "Retard moyen de tous les trains au départ"])


def test_preprocess_duplicated_rows(mocked_raw_sncf_df) -> None:
    """Test the merging of the duplicated observations / rows
    for the same month and train line."""

    # create 2 observations for the same month and train line
    df = mocked_raw_sncf_df.iloc[[0, 0]].copy().reset_index(drop=True)

    df["Date"] = ["2025-07-01", "2025-07-01"]
    df["Service"] = ["National", "International"]

    df["Nombre de circulations prévues"] = [100, 200]
    df["Nombre de trains annulés"] = [5, 10]
    df["Nombre de trains en retard à l'arrivée"] = [10, 30]
    df["Retard moyen des trains en retard à l'arrivée"] = [20.0, 40.0]
    df["Nombre trains en retard > 60min"] = [1, np.nan]

    df["Durée moyenne du trajet"] = [120.0, 120.0]
    df["Retard moyen trains en retard > 15 (si liaison concurrencée par vol)"] = [
        25.0,
        35.0,
    ]

    result = preprocess_data(df)

    # check that the 2 observations are merged
    assert len(result) == 1

    # check the sums
    assert result.iloc[0]["Nombre de circulations prévues"] == 300
    assert result.iloc[0]["Nombre de trains annulés"] == 15
    assert result.iloc[0]["Nombre de trains en retard à l'arrivée"] == 40
    # check the sum when one value is NaN
    assert result.iloc[0]["Nombre trains en retard > 60min"] == 1

    # check the weighted mean delay
    assert result.iloc[0]["Retard moyen des trains en retard à l'arrivée"] == 35.0

    # check that the service is NaN
    assert pd.isna(result.iloc[0]["Service"])


def test_preprocess_error_duplicated_rows(mocked_raw_sncf_df) -> None:
    """Test that unexpected duplicated rows raise an error."""

    # create 2 observations with the same month, train line and service
    df = mocked_raw_sncf_df.iloc[[0, 0]].copy().reset_index(drop=True)

    df["Date"] = ["2025-07-01", "2025-07-01"]
    df["Service"] = ["National", "National"]

    # check that the error is raised
    with pytest.raises(ValueError, match="Unexpected duplicate route"):
        preprocess_data(df)
