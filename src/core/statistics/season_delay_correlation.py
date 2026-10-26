import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa import statespace as sp
from sklearn.metrics import mean_squared_error, mean_absolute_error

from core import load_data as ld

def compute_arrival_mean_delay_history_from_city_pair(departure:str, arrival:str):
    """_summary_

    Args:
        departure (str): _description_
        arrival (str): _description_

    Returns:
        list: A list of tuple under format [(month_1, mean_arrival_delay_1), ... , (month_N, mean_arrival_delay_N)]
    """
    global arrival_mean_delay_history_for_current_city_pair

    # filter data with departure and arrival cities features
    departure_df = ld.df[ld.df[ld.DEPARTURE_STATION_KEY] == departure]
    departure_arrival_df = departure_df[departure_df[ld.ARRIVAL_STATION_KEY] == arrival]

    # filter data with departure and arrival cities features
    date_df = departure_arrival_df[ld.DATE_KEY]
    mean_arrival_delay_df = departure_arrival_df[ld.MEAN_ARRIVAL_DELAY_KEY]

    # build list from data to plot in matplotlib
    date_list = date_df.values
    mean_arrival_delay_list = mean_arrival_delay_df.values
    arrival_mean_delay_history_for_current_city_pair = list(zip(date_list, mean_arrival_delay_list))

    return arrival_mean_delay_history_for_current_city_pair


def get_arrival_mean_delay_history_from_city_pair() -> list:
    return arrival_mean_delay_history_for_current_city_pair