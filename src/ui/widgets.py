"""User interactions widgets definition module"""

import streamlit as st
import numpy as np

from core import load_data as ld
from core.statistics import amount_trains as am


MONTHS_LIST = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

def section_row(section_label: str, fields: list) -> None:
    """Displays information contained in fields input, named after section_label input, 
    under the format of a 2 columns table : | section_label | field1
                                            |               | field2
                                            |               | ....
                                            |               | fieldN
                                            
    If the trains delayed/cancelled count is greater than 0, the statistic is displayed
    with associated string. Otherwise, "none" is output.

    Args:
        section_label (str): Label of the section, contained in the first column. 
        This field is formatted as follows: count (# of delayed/cancelled trains), total
        (# of planned trains on the period and given the cities) 
        and status (string adapted to the stat to be displayed at reader)
        
        fields (list): list of fields. First field is displayed in the second column, 
        same line as the section_label. Other fields are stacked on the following rows 
        on the second column.
    """
    
    cols = st.columns([1, 2])
    cols[0].markdown(f"**{section_label}**")
    
    for index, (count, total, status) in enumerate(fields):
    # for index, (label, count, total, status) in enumerate(fields):

        if count > 0:
            ratio_tot_cnt_trains = total/count
            train_info_str = (
                f"1 out of {round(ratio_tot_cnt_trains)} trains were {status}"
            )
        elif np.isnan(total):
            train_info_str = "No data is available"
        else: 
            train_info_str = f"No {status} train was declared"

        if index == 0:
            # cols[1].markdown(label)
            with cols[1]:
                st.write(train_info_str)
        else:
            _, sub_input_col = st.columns([1, 2])
            # _, sub_label_col, sub_input_col = st.columns([1, 2, 3])
            # sub_label_col.markdown(label)
            with sub_input_col:
                st.write(train_info_str)

def select_month(msg: str) -> int:
    """Get month from a dropdown list as integer, requiring get_month_from_str_int
    function to convert a month string to integer for further functions.

    Args:
        msg (str): Message to be displayed aside the dropdown list

    Returns:
        selected_month (int): Selected month as integer (bewteen 1 and 12)
    """

    selected_month = get_month_from_str_int(st.selectbox(msg, MONTHS_LIST))
    
    return selected_month

def select_years(msg: str) -> list[int]:
    """Get year(s) from a multiselect dropdown.
    Initially, all years from the dataset are selected.

    Args:
        msg (str): Message to be displayed aside the dropdown list

    Returns:
        selected_years (list[int]): Selected years from the initialized dataset.
    """

    years = sorted(ld.df.year.unique())

    return st.multiselect(msg, options=years, default=years)

def get_month_from_int_str(month_int: int) -> str:
    """Converts a month as integer into string.
    This is based on a dictionnary month_dict{month_int: month_str}

    Args:
        month_int (int): month as integer

    Returns:
        month_str (str): month as string
    """
    
    month_dict = {
        index: month
        for index, month in enumerate(MONTHS_LIST, start=1)
        if month
    }
    month_str = month_dict[month_int]
    
    return month_str

def get_month_from_str_int(month_str: str) -> int:
    """Converts a month as string into integer. 
    This is based on a dictionnary month_dict{month_str: month_int}

    Args:
        month_str (str): month as string

    Returns:
        month_int (int): month as integer
    """
    
    month_dict = {
        month: index for index, 
        month in enumerate(MONTHS_LIST, start=1) 
        if month
    }
    month_int = month_dict[month_str]
    
    return month_int

def display_sidebar() -> list:
    """Displays sidebar containing input widgets for customer to specify 
    a trip to vizualize
    
    Returns:
        trip_infos (np.array): array of trip infos departure_city, arrival_city, 
        start_month, end_month, selected_years
    """
    
    with st.sidebar:
        st.set_page_config(initial_sidebar_state="expanded")

        st.sidebar.title("Tell us more about your trip")
        
        departure_city = st.selectbox(
                    "Departure:",
                    ld.get_unique_railstations_df(),
                )
        arrival_city = st.selectbox(
                    "Destination:",
                    ld.get_reachable_destinations_list_from_city(departure_city),
                )
        start_month = select_month("Period from:")
        end_month = select_month(" to:")
        selected_years = select_years("Years:")
        trip_infos = [departure_city, arrival_city, start_month, end_month, 
                               selected_years]
        
        return trip_infos
        
def display_delayed_cancelled_stats_table(col: str, departure_city: str, 
                                          arrival_city: str, start_month: str, 
                                          end_month: str, 
                                          selected_years: np.array) -> None:
    """Displays in the given col column a table displaying a ratio formatted as 1 out
    of X, where X being total departure delayed/cancelled 
    and arrival delayed trains amount.
    The statistics are the mean values computed over a given months/years period, 
    for a given departure and arrival cities.

    Args:
        col (str): body column number to place the table
        departure_city (str): departure city to compute the statistics
        arrival_city (str): arrival city
        start_month (str): first month of the time period for a given year
        end_month (str): last month of the time period
        selected_years (np.array): np.array of selected years to compute the statistics
    """
    with col:
        st.markdown(f"## {departure_city.title()} --> {arrival_city.title()}\n### Traffic state info ")
        
        total_planned_trains = am.get_total_planned_trains(
            departure_city, arrival_city, start_month, end_month, selected_years)
            
        st.markdown(f"Over the period from "
                    f"{get_month_from_int_str(start_month)} to "
                    f" {get_month_from_int_str(end_month)}:")

        # Departure: Delay + Cancelled
        section_row("Departure", [
            (am.get_total_delayed_departure_trains(departure_city, arrival_city, 
                                                            start_month, end_month, 
                                                            selected_years),
            total_planned_trains, "delayed"),
            (am.get_total_cancelled_trains(departure_city, arrival_city, 
                                                            start_month, end_month, 
                                                            selected_years),
            total_planned_trains, "cancelled"),
        ])

        st.divider()

        # Arrival: Delay only
        section_row("Arrival", [
            (am.get_total_delayed_arrival_trains(departure_city, arrival_city, 
                                                                start_month, end_month, 
                                                                selected_years),
            total_planned_trains, "delayed"),
        ])