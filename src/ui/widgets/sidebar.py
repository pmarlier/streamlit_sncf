"""Module defining the sidebar components. The sidebar is initialized open, and lets the
user specifiy a trip to analyse with its:
    - departure station
    - arrival station
    - departure month
    - arrival month (equal or posterior to departure month)
    - years

Those data are used to compute statistics on a given connexion, based on all the
previous selected periods."""

import logging.config

import streamlit as st

from core import load_data as ld

MONTHS_LIST = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


def init() -> None:
    """
    Initialization function to set logger
    """
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)
    logger.debug("sidebar logger initialized")


@st.dialog("Erreur de période !")
def wrong_month_dialog():
    """Popup window function used for months selection functions, to explain to the user
    that the selected departure month must be equal or prior to arrival month.
    """
    st.write("Le mois de départ doit être égal ou antérieur au mois d'arrivée.")
    logger.warning("Bad use of widget")


@st.dialog("Aucune année sélectionnée !")
def no_year_dialog():
    """Popup window function used for years selection functions, to explain to the user
    that at least one year shall be selected to generate stats.
    """
    st.write("Sélectionnez au moins une année.")
    logger.warning("Bad use of widget")


def get_month_from_int_str(month_int: int) -> str:
    """Converts a month as integer into string.
    This is based on a dictionnary month_dict{month_int: month_str}

    Args:
        month_int (int): month as integer

    Returns:
        month_str (str): month as string
    """

    month_dict = {
        index: month for index, month in enumerate(MONTHS_LIST, start=1) if month
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
        month: index for index, month in enumerate(MONTHS_LIST, start=1) if month
    }
    month_int = month_dict[month_str]

    return month_int


def select_month(msg: str, index: int) -> int:
    """Get month from a dropdown list as integer, requiring get_month_from_str_int
    function to convert a month string to integer for further functions.

    Args:
        msg (str): Message to be displayed aside the dropdown list
        index (str): The index of the preselected option on first render.

    Returns:
        selected_month (int): Selected month as integer (bewteen 1 and 12)
    """

    selected_month = get_month_from_str_int(st.selectbox(msg, MONTHS_LIST, index))

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


def display_sidebar() -> None:
    """Displays sidebar containing input widgets for customer to specify
    a trip to vizualize

    Returns:
        trip_infos (np.array): array of trip infos departure_city, arrival_city,
        start_month, end_month, selected_years
    """

    st.sidebar.title("Quelles villes souhaitez-vous relier ?")

    st.session_state.departure_city = st.selectbox(
        "Ville de départ :",
        ld.get_unique_railstations_df(),
    )
    logger.debug(f"{st.session_state.departure_city} departure city selected")

    st.session_state.arrival_city = st.selectbox(
        "Ville de destination :",
        ld.get_reachable_destinations_list_from_city(st.session_state.departure_city),
    )
    logger.debug(f"{st.session_state.arrival_city} arrival city selected")

    st.session_state.start_month = select_month(
        "Traitement des données entre le mois de :", 0
    )
    logger.debug(
        f"{get_month_from_int_str(st.session_state.start_month)} departure month selected"
    )

    st.session_state.end_month = select_month(" et de :", 11)
    if st.session_state.end_month < st.session_state.start_month:
        wrong_month_dialog()
        logger.warning(
            f"Warning: {get_month_from_int_str(st.session_state.end_month)} arrival month is "
            "anterior to departure month, try again..."
        )
    logger.debug(
        f"{get_month_from_int_str(st.session_state.end_month)} arrival month selected"
    )

    st.session_state.selected_years = select_years("pour les années :")

    if not st.session_state.selected_years:
        no_year_dialog()
        logger.warning("Warning: at least one year shall be selected")

    logger.debug(
        f"Years selected: {', '.join(map(str, st.session_state.selected_years))}"
    )

    # Bouton personnalisé pour basculer l'état
    if st.button("Retour à la page d'accueil", width="stretch"):
        st.session_state.is_trip_set = False
        st.rerun()

    return
