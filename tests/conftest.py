import numpy as np
import pandas as pd
import pytest

from core import load_data as ld


@pytest.fixture
def mocked_df() -> pd.DataFrame:
    """Small sample matching the dataframe returned by load_csv_df.

    On top of the regular 2018-2020 samples, the dataframe contains:
    - 2019 rows with partially missing (np.nan) metrics,
    - an "empty" year 2021 where every metric is np.nan.
    """
    base_df = pd.DataFrame(
        {
            ld.YEAR_KEY: [
                2018,
                2018,
                2018,
                2018,
                2019,
                2019,
                2019,
                2019,
                2020,
                2020,
                2020,
                2020,
            ],
            ld.MONTH_KEY: [1, 2, 3, 1, 1, 2, 3, 4, 1, 2, 3, 12],
            ld.DEPARTURE_STATION_KEY: [
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "RENNES",
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "BORDEAUX ST JEAN",
                "PARIS MONTPARNASSE",
                "RENNES",
                "PARIS MONTPARNASSE",
                "NANTES",
            ],
            ld.ARRIVAL_STATION_KEY: [
                "RENNES",
                "RENNES",
                "RENNES",
                "PARIS MONTPARNASSE",
                "RENNES",
                "RENNES",
                "BORDEAUX ST JEAN",
                "PARIS MONTPARNASSE",
                "RENNES",
                "PARIS MONTPARNASSE",
                "NANTES",
                "PARIS MONTPARNASSE",
            ],
            ld.MEAN_DEPARTURE_DELAY_KEY: [
                10.08860759,
                18.19316239,
                10.47901961,
                7.589985994,
                9.8,
                12.4,
                11.2,
                8.6,
                10.2,
                8.8,
                9.5,
                7.1,
            ],
            ld.MEAN_ARRIVAL_DELAY_KEY: [
                21.10280374,
                34.35,
                25.31081081,
                18.50022523,
                20.1,
                26.3,
                24.6,
                19.2,
                22.5,
                19.8,
                23.1,
                18.7,
            ],
            ld.MONTHLY_CANCELLED_TRAINS_KEY: [
                1,  # 2018 PM -> R
                32,  # 2018 PM -> R
                17,  # 2018 PM -> R
                4,  # 2018 R -> PM
                2,
                8,
                3,
                1,
                6,  # 2020 PM -> R
                4,
                5,
                2,
            ],
            ld.MONTHLY_PLANNED_TRAINS_KEY: [
                590,  # 2018 PM -> R
                547,  # 2018 PM -> R
                599,  # 2018 PM -> R
                599,  # 2018 R -> PM
                580,
                565,
                603,
                590,
                610,  # 2020 PM -> R
                602,
                615,
                625,
            ],
            ld.MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY: [
                79,  # 2018 PM -> R
                117,  # 2018 PM -> R
                85,  # 2018 PM -> R
                238,  # 2018 R -> PM
                86,
                105,
                92,
                71,
                98,  # 2020 PM -> R
                82,
                108,
                77,
            ],
            ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY: [
                107,  # 2018 PM -> R
                156,  # 2018 PM -> R
                74,  # 2018 PM -> R
                148,  # 2018 R -> PM
                96,
                112,
                88,
                73,
                119,  # 2020 PM -> R
                95,
                104,
                81,
            ],
            ld.MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT: [
                10.0,  # 2018
                20.0,  # 2018
                30.0,  # 2018
                40.0,  # 2018
                10.0,
                20.0,
                30.0,
                40.0,
                10.0,  # 2020 PM -> R
                20.0,
                30.0,
                40.0,
            ],
            ld.MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT: [
                5.0,  # 2018
                15.0,  # 2018
                25.0,  # 2018
                35.0,  # 2018
                5.0,
                15.0,
                25.0,
                35.0,
                5.0,  # 2020 PM -> R
                15.0,
                25.0,
                35.0,
            ],
            ld.MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT: [
                2.0,  # 2018
                12.0,  # 2018
                22.0,  # 2018
                32.0,  # 2018
                2.0,
                12.0,
                22.0,
                32.0,
                2.0,  # 2020 PM -> R
                12.0,
                22.0,
                32.0,
            ],
            ld.MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT: [
                1.0,  # 2018
                11.0,  # 2018
                21.0,  # 2018
                31.0,  # 2018
                1.0,
                11.0,
                21.0,
                31.0,
                1.0,  # 2020 PM -> R
                11.0,
                21.0,
                31.0,
            ],
            ld.MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT: [
                0.0,  # 2018
                10.0,  # 2018
                20.0,  # 2018
                30.0,  # 2018
                0.0,
                10.0,
                20.0,
                30.0,
                0.0,  # 2020 PM -> R
                10.0,
                20.0,
                30.0,
            ],
            ld.MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT: [
                100.0,  # 2018
                200.0,  # 2018
                300.0,  # 2018
                400.0,  # 2018
                100.0,
                200.0,
                300.0,
                400.0,
                100.0,  # 2020 PM -> R
                200.0,
                300.0,
                400.0,
            ],
            ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT: [
                50.0,  # 2018
                150.0,  # 2018
                250.0,  # 2018
                350.0,  # 2018
                50.0,
                150.0,
                250.0,
                350.0,
                50.0,  # 2020 PM -> R
                150.0,
                250.0,
                350.0,
            ],
        }
    )

    # Extra samples with missing (np.nan) values, on already existing trips
    # and outside the 2018/2020 periods asserted by the statistics tests:
    # - 2019: two partially missing samples (some metrics are np.nan)
    # - 2021: an "empty" year, where every metric is np.nan
    nan_samples_df = pd.DataFrame(
        {
            ld.YEAR_KEY: [2019, 2019, 2021, 2021],
            ld.MONTH_KEY: [5, 6, 3, 9],
            ld.DEPARTURE_STATION_KEY: [
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "PARIS MONTPARNASSE",
                "RENNES",
            ],
            ld.ARRIVAL_STATION_KEY: [
                "RENNES",
                "RENNES",
                "RENNES",
                "PARIS MONTPARNASSE",
            ],
            ld.MEAN_DEPARTURE_DELAY_KEY: [np.nan, 10.3, np.nan, np.nan],
            ld.MEAN_ARRIVAL_DELAY_KEY: [22.4, np.nan, np.nan, np.nan],
            ld.MONTHLY_CANCELLED_TRAINS_KEY: [np.nan, 7, np.nan, np.nan],
            ld.MONTHLY_PLANNED_TRAINS_KEY: [598, np.nan, np.nan, np.nan],
            ld.MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY: [np.nan, 95, np.nan, np.nan],
            ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY: [90, np.nan, np.nan, np.nan],
            ld.MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT: [10.0, np.nan, np.nan, np.nan],
            ld.MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT: [
                np.nan,
                15.0,
                np.nan,
                np.nan,
            ],
            ld.MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT: [
                2.0,
                np.nan,
                np.nan,
                np.nan,
            ],
            ld.MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT: [
                np.nan,
                11.0,
                np.nan,
                np.nan,
            ],
            ld.MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT: [
                0.0,
                np.nan,
                np.nan,
                np.nan,
            ],
            ld.MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT: [
                np.nan,
                200.0,
                np.nan,
                np.nan,
            ],
            ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT: [
                50.0,
                np.nan,
                np.nan,
                np.nan,
            ],
        }
    )

    return pd.concat([base_df, nan_samples_df], ignore_index=True)


@pytest.fixture
def mocked_railway_geo_df() -> pd.DataFrame:
    """Mock for lignes-par-region-administrative.csv to draw precise railway
    Sample of the real file, only for used column

    Note: the geodata is really store in the reverse mode long, lat instead of lat, long
    The source code reverses data

    ["CODE_LIGNE"] ; ["Geo Shape"]
    472000;"{""coordinates"": [[-2.273912474801684, 48.08279287107057],
     [-2.26935619345393, 48.0858985269676],
     [-2.269125456095638, 48.08605656053114],
     [-2.26759295199921, 48.08710613934727],
     [-2.266720660819492, 48.08769735744491],
     [...]
     [-2.213833057941379, 48.133309853158316],
     [-2.211657412817431, 48.135240690831694],
     [-2.211210777587779, 48.1356370467141],
     [-2.210813213953706, 48.13596702835614],
     [...]
     [-2.209968342517308, 48.16152465585667],
     [-2.209614954555336, 48.16237119747858],
     [-2.208637875746816, 48.16412238332462],
     [-2.207459803104205, 48.16618070340646],
     [...]
     [-2.16078439639358, 48.20152271869188],
     [-2.156399464750506, 48.204185445713534],
     [-2.153757717946701, 48.205758886706256],
     [...]
     [-2.11687544430763, 48.215876496003155],
     [-2.114505509976158, 48.21494072374514],
     [-2.108385722229834, 48.21236721558984],
     [-2.107153829639365, 48.21210514836861]],
     ""type"": ""LineString""}"
    """
    return pd.DataFrame(
        {
            "CODE_LIGNE": [101, 102, 103, 104, 105],
            "Geo Shape": [
                # perfect railway coordinates where both railstations are
                # the beginning and the end of the path (101)
                # Note (again): coordinates are really stored in long, lat format.....
                '{"coordinates": [[2.3, 48.8], [1.6, 48.4]], "type": "LineString"}',
                # special lines for edge case testing : empty line, (105)
                # railway coordinates exceed railstation coordinates (102 and 103)
                # railway coordinates that doesn't fit the trip at all (105)
                '{"coordinates": [[3.0, 49.5], [2.3, 48.8], [1.6, 48.4]], "type": "LineString"}',
                '{"coordinates": [[2.3, 48.8], [1.6, 48.4], [1.0, 47.0]], "type": "LineString"}',
                '{"coordinates": [[10.0, 50.0], [11.0, 51.0]], "type": "LineString"}',
                '{"coordinates": [], "type": "LineString"}',
            ],
        }
    )


@pytest.fixture
def mocked_railstation_geo_df() -> pd.DataFrame:
    """Mock for liste-des-gares.csv to get railstation geographic coordinates
    Sample of the real file, only for the used column

    ["LIBELLE"] ; ["Geo Point"]

    [...];LIBELLE;[...];Geo Point

    Paris-Montparnasse-Pasteur;48.83921287344567, 2.3181430216303696
    Rennes;48.10337713690151, 1.67082488618460
    Bordeaux-St-Jean;44.825923101976585, 0.5559775161877943

    """
    return pd.DataFrame(
        {
            "LIBELLE": ["paris-montparnasse-pasteur", "rennes", "bordeaux-st-jean"],
            "Geo Point": ["48.8, 2.3", "48.4, 1.6", "44.8, 0.5"],
        }
    )
