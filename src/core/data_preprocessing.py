import pandas as pd
import numpy as np


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess a dataframe to clean the data. It has been designed to preprocess the SNCF dataset.

    Transformations :
    1. Invalidate the data from the Covid period
    2. Invalidate the data from the columns "Nombre trains en retard > 30min" and "Nombre trains en retard > 60min"
    in Q1 2025
    3. If no train is delayed at arrival, replacing 0 values of average delay by NaN
    4. If no train is delayed at departure, invalidating values of average delay by NaN
    5. Imputing historical median if trains are delayed but the average delay
    "Retard moyen des trains en retard à l'arrivée" is less than or equal to 0.
    The median is calculated for the same service, route and month, with at least 2 valid observations.
    6. Adding a column "Prct retard causes non renseignées" and calculating the percentage
    to have a sum of 100% for all the reasons of delay

    Args:
        df (pd.DataFrame): dataframe from the original SNCF dataset with these expected columns at least :
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
            "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)"

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

    # Selecting valid observations and calculating medians and counts in the different groups

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

    # Sixth evolution : adding a column "Prct retard causes non renseignées"

    columns_reasons = [
        "Prct retard pour causes externes",
        "Prct retard pour cause infrastructure",
        "Prct retard pour cause gestion trafic",
        "Prct retard pour cause matériel roulant",
        "Prct retard pour cause gestion en gare et réutilisation de matériel",
        "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)",
    ]

    # Calculating the sum of the 6 reasons

    sum_reasons = df_clean[columns_reasons].sum(axis=1, min_count=len(columns_reasons))

    # Adding the new column

    df_clean["Prct retard causes non renseignées"] = (
        (100 - sum_reasons).round(2).where(df_clean[delayed_trains_arr] > 0)
    )

    # Returning df_clean

    return df_clean
