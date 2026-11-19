import numpy as np
import pandas as pd


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess a dataframe to clean the data.
    It has been designed to preprocess the SNCF dataset.

    Transformations :

    1. Invalidate the data from the Covid period

    2. Invalidate the data from the columns "Nombre trains en retard > 30min" and
    "Nombre trains en retard > 60min" in Q1 2025

    3. If no train is delayed at arrival, replacing 0 values of average delay by NaN

    4. If no train is delayed at departure, invalidating values of average delay by NaN

    5. Imputing historical median if trains are delayed but the average delay
    "Retard moyen des trains en retard à l'arrivée" is less than or equal to 0.
    The median is calculated for the same service, route and month, with at least 2
    valid observations.

    6. Invalidating values from "Nombre trains en retard > 15min" when they exceed the
    overall number of trains delayed at arrival.

    7. Replacing negative average delays for all trains by 0 when they are between -1
    (included) and 0 (excluded), and by NaN when they are below -1.

    8. Merge the duplicated rows

    9. Adding a column "Prct retard causes non renseignées" and calculating the
    percentage to have a sum of 100% for all the reasons of delay

    Args:
        df (pd.DataFrame): dataframe from the original SNCF dataset with these expected
        columns at least :
            "Date",
            "Service",
            "Gare de départ",
            "Gare d'arrivée",
            "Nombre de trains en retard à l'arrivée",
            "Nombre de trains en retard au départ",
            "Nombre trains en retard > 30min",
            "Nombre trains en retard > 60min",
            "Retard moyen des trains en retard à l'arrivée",
            "Retard moyen des trains en retard au départ",
            "Prct retard pour causes externes",
            "Prct retard pour cause infrastructure",
            "Prct retard pour cause gestion trafic",
            "Prct retard pour cause matériel roulant",
            "Prct retard pour cause gestion en gare et réutilisation de matériel",
            "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH,
            correspondances)",
            "Nombre trains en retard > 15min",
            "Retard moyen de tous les trains à l'arrivée",
            "Retard moyen de tous les trains au départ",

    Returns:
        pd.DataFrame: a dataframe with the applied transformations
    """

    df_clean = df.copy()
    df_clean["Date"] = pd.to_datetime(df_clean["Date"])

    # First evolution : invalidating data (transforming as NaN) from Covid period
    mask_covid = (df_clean["Date"] >= "2020-03-01") & (df_clean["Date"] < "2021-07-01")

    columns_selection_covid = ["Date", "Gare de départ", "Gare d'arrivée", "Service"]

    columns_data = [
        col for col in df_clean.columns if col not in columns_selection_covid
    ]

    df_clean.loc[mask_covid, columns_data] = np.nan

    # Second evolution : invalidating data from Q1 2025
    mask_q1_2025 = (df_clean["Date"] >= "2025-01-01") & (
        df_clean["Date"] < "2025-04-01"
    )

    columns_selection_q1_2025 = [
        "Nombre trains en retard > 30min",
        "Nombre trains en retard > 60min",
    ]

    df_clean.loc[mask_q1_2025, columns_selection_q1_2025] = np.nan

    # Third evolution : when no train is delayed at arrival,
    # replacing 0 values of average delay by NaN

    delayed_trains_arr = "Nombre de trains en retard à l'arrivée"
    average_delay_arr = "Retard moyen des trains en retard à l'arrivée"

    mask_zero_delayed_trains = (df_clean[delayed_trains_arr] == 0) & (
        df_clean[average_delay_arr] == 0
    )

    df_clean.loc[mask_zero_delayed_trains, average_delay_arr] = np.nan

    # Fourth evolution : when no train is delayed at departure,
    # invalidating values of average delay by NaN

    delayed_trains_dep = "Nombre de trains en retard au départ"
    average_delay_dep = "Retard moyen des trains en retard au départ"

    mask_zero_delay_dep = (df_clean[delayed_trains_dep] == 0) & (
        df_clean[average_delay_dep].notna()
    )

    df_clean.loc[mask_zero_delay_dep, average_delay_dep] = np.nan

    # Fifth evolution : if trains are delayed but
    # the average delay "Retard moyen des trains en retard à l'arrivée"
    # is <=0 then it imputs historical median

    # Identifying invalid averages

    mask_imputation = (df_clean[delayed_trains_arr] > 0) & (
        df_clean[average_delay_arr] <= 0
    )

    # Selecting valid observations and calculating medians and counts
    # in the different groups

    references = df_clean[
        (df_clean["Date"].dt.year.between(2018, 2025))
        & (df_clean[delayed_trains_arr] > 0)
        & (df_clean[average_delay_arr] > 0)
    ]

    groups = references.groupby(
        ["Service", "Gare de départ", "Gare d'arrivée", references["Date"].dt.month]
    )[average_delay_arr]

    medians = groups.median()
    groups_counts = groups.count()

    # Invalidating the original values
    # and if we have a minimum of 2 values in the past, then replacing with the median

    df_clean.loc[mask_imputation, average_delay_arr] = np.nan

    for i in df_clean.index[mask_imputation]:
        line = df_clean.loc[i]

        line_chatacteristics = (
            line["Service"],
            line["Gare de départ"],
            line["Gare d'arrivée"],
            line["Date"].month,
        )

        if groups_counts.get(line_chatacteristics, 0) >= 2:
            df_clean.loc[i, average_delay_arr] = medians[line_chatacteristics]

    # Sixth evolution: invalidating number of trains delayed by more than 15 minutes
    # when they are greater than the total number of trains delayed at arrival

    delayed_trains_15 = "Nombre trains en retard > 15min"

    mask_invalid_15 = df_clean[delayed_trains_15] > df_clean[delayed_trains_arr]

    df_clean.loc[mask_invalid_15, delayed_trains_15] = np.nan

    # Seventh evolution: transforming negative values in columns
    # "Retard moyen de tous les trains à l'arrivée" and "Retard moyen de tous les trains
    # au départ"

    columns_average_delay = [
        "Retard moyen de tous les trains à l'arrivée",
        "Retard moyen de tous les trains au départ",
    ]

    threshold_clean = -1

    # the negative values between the threshold and 0 (excluded) are converted to 0
    # the negative values below the threshold are converted to NaN
    for col in columns_average_delay:
        mask_zero = (df_clean[col] >= threshold_clean) & (df_clean[col] < 0)

        mask_nan = df_clean[col] < threshold_clean

        df_clean.loc[mask_zero, col] = 0.0
        df_clean.loc[mask_nan, col] = np.nan

    # columns used in eighth and ninth evolutions

    columns_reasons = [
        "Prct retard pour causes externes",
        "Prct retard pour cause infrastructure",
        "Prct retard pour cause gestion trafic",
        "Prct retard pour cause matériel roulant",
        "Prct retard pour cause gestion en gare et réutilisation de matériel",
        (
            "Prct retard pour cause prise en compte voyageurs "
            "(affluence, gestions PSH, correspondances)"
        ),
    ]

    # Eighth evolution: merging duplicated observations

    # import which needs to be done later in the process
    from core.statistics import mean_delay as md

    columns_duplicates = [
        "Date",
        "Gare de départ",
        "Gare d'arrivée",
    ]

    mask_duplicates = df_clean.duplicated(
        subset=columns_duplicates,
        keep=False,
    )

    # columns containing counts
    columns_to_sum = [
        "Nombre de circulations prévues",
        "Nombre de trains annulés",
        "Nombre de trains en retard au départ",
        "Nombre de trains en retard à l'arrivée",
        "Nombre trains en retard > 15min",
        "Nombre trains en retard > 30min",
        "Nombre trains en retard > 60min",
    ]

    merged_rows = []

    for _, group in df_clean.loc[mask_duplicates].groupby(columns_duplicates):
        # checking that there are 2 different services for the same train line
        if len(group) != 2 or set(group["Service"]) != {"National", "International"}:
            raise ValueError("Unexpected duplicate route")

        # creating the merged row from the first observation
        merged_row = group.iloc[0].copy()
        merged_row["Service"] = np.nan

        # replacing NaN with 0 before calculations
        data = group.select_dtypes(include="number").fillna(0)

        # sum of train counts
        for col in columns_to_sum:
            merged_row[col] = data[col].sum()

        # calculating the weights for the weighted means
        completed_trains = (
            data["Nombre de circulations prévues"] - data["Nombre de trains annulés"]
        ).clip(lower=0)

        delayed_departure = data["Nombre de trains en retard au départ"]
        delayed_arrival = data["Nombre de trains en retard à l'arrivée"]
        delayed_15 = data["Nombre trains en retard > 15min"]

        # calculating the weighted mean for all completed trains
        columns_completed_trains = [
            "Durée moyenne du trajet",
            "Retard moyen de tous les trains au départ",
            "Retard moyen de tous les trains à l'arrivée",
        ]

        for col in columns_completed_trains:
            merged_row[col] = md.weighted_mean_delay(completed_trains, data[col])

        # calculating the weighted mean for trains delayed at departure
        col = "Retard moyen des trains en retard au départ"
        merged_row[col] = md.weighted_mean_delay(delayed_departure, data[col])

        # calculating the weighted mean for trains delayed at arrival
        col = "Retard moyen des trains en retard à l'arrivée"
        merged_row[col] = md.weighted_mean_delay(delayed_arrival, data[col])

        # calculating the weighted mean for trains delayed by more than 15 minutes
        col = "Retard moyen trains en retard > 15 (si liaison concurrencée par vol)"
        merged_row[col] = md.weighted_mean_delay(delayed_15, data[col])

        # calculating the weighted percentages for delay causes
        for col in columns_reasons:
            merged_row[col] = md.weighted_mean_delay(delayed_arrival, data[col])

        merged_rows.append(merged_row)

    # replacing duplicated rows with the merged rows
    if len(merged_rows) > 0:
        df_clean = (
            pd.concat(
                [
                    df_clean.loc[~mask_duplicates],
                    pd.DataFrame(merged_rows),
                ]
            )
            .sort_index()
            .reset_index(drop=True)
        )

    # Ninth evolution : adding a column "Prct retard causes non renseignées"

    # Calculating the sum of the 6 reasons

    sum_reasons = df_clean[columns_reasons].sum(axis=1, min_count=len(columns_reasons))

    # Adding the new column

    df_clean["Prct retard causes non renseignées"] = (
        (100 - sum_reasons).round(2).where(df_clean[delayed_trains_arr] > 0)
    )

    # Returning df_clean

    return df_clean
