import logging.config

from core import load_data as ld


def init() -> None:
    """Initialize logger and set dataframe imported from CSV files"""
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)
    logger.debug("logger set")


def get_mean_cause_list(departure_city: str = None, arrival_city: str = None) -> list:
    """Retrieve the list of all the delay causes and
    their frequency of occurrence known for a given city pair.

    If no city pair is given, return all the delay causes and
    their frequency of occurrence over all the network

    Args:
        departure_city (str, optional): the departure city of the railway to analyze
        Defaults to None.
        arrival_city (str, optional): the arrival city of the railway to analyze
        Defaults to None.

    Returns:
        list: the list of all the delay causes and
    their frequency of occurrence known for a given city pair,
    or over all the french network (depending on the given args).
    The order of causes is given hereafter :
            external
            infrastructural
            traffic_management
            mobile_equipment
            railstation_management
            traveler
            unknown
    """
    cause_list = [
        get_mean_of_external_cause(departure_city, arrival_city),
        get_mean_of_infrastructural_cause(departure_city, arrival_city),
        get_mean_of_traffic_management_cause(departure_city, arrival_city),
        get_mean_of_mobile_equipment_cause(departure_city, arrival_city),
        get_mean_of_railstation_management_cause(departure_city, arrival_city),
        get_mean_of_traveler_cause(departure_city, arrival_city),
        get_mean_of_unknown_cause(departure_city, arrival_city),
    ]

    logger.debug(
        "Whole delay cause list retrieved "
        f"for railway {departure_city} - {arrival_city}"
    )

    return cause_list


def get_mean_of_external_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of externally caused delay
    known for a given city pair.

        If no city pair is given, return the frequency of externally caused delay
    over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of externally caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_infrastructural_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of infrastructural caused delay
    known for a given city pair.

        If no city pair is given, return the frequency of infrastructural caused delay
    over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of infrastructural caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_traffic_management_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of traffic management caused delay
    known for a given city pair.

    If no city pair is given, return the frequency of traffic management caused delay
    over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of traffic management caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_mobile_equipment_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of mobile equipment failure caused delay
    known for a given city pair.

        If no city pair is given, return the frequency of mobile equipment failure
        caused delay over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of mobile equipment failure caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_railstation_management_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of railstation management caused delay
    known for a given city pair.

        If no city pair is given, return the frequency of railstation management
        caused delay over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of railstation management caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_traveler_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Retrieve the frequency of traveler caused delay
    known for a given city pair.

        If no city pair is given, return the frequency of traveler
        caused delay over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of traveler caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT].mean()
    )


def get_mean_of_unknown_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
    """Sometimes, the sum of delay cause frequency given by SNCF does not sum to 100%
    The unlabeled missing part is said to be from an unknown cause
    Retrieve the frequency of unkown caused delay
    known for a given city pair.

    If no city pair is given, return the frequency of unkown
    caused delay over all the network

        Args:
            departure_city (str, optional): the departure city of the railway to analyze
            Defaults to None.
            arrival_city (str, optional): the arrival city of the railway to analyze
            Defaults to None.

        Returns:
            float: the frequency of unkown caused delay
            known for a given city pair,
            or over all the french network (depending on the given args).
    """
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT].mean()
    )
