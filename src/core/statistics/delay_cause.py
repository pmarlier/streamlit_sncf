from core import load_data as ld


def get_mean_cause_list(departure_city: str = None, arrival_city: str = None) -> list:
    cause_list = [
        get_mean_of_external_cause(departure_city, arrival_city),
        get_mean_of_infrastructural_cause(departure_city, arrival_city),
        get_mean_of_traffic_management_cause(departure_city, arrival_city),
        get_mean_of_mobile_equipment_cause(departure_city, arrival_city),
        get_mean_of_railstation_management_cause(departure_city, arrival_city),
        get_mean_of_traveler_cause(departure_city, arrival_city),
        get_mean_of_unknown_cause(departure_city, arrival_city),
    ]
    return cause_list


def get_mean_of_external_cause(
    departure_city: str = None, arrival_city: str = None
) -> float:
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
    df = ld.get_monthly_stats_df()
    return (
        df[ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT].mean()
        if (departure_city is None or arrival_city is None)
        else df[
            (df[ld.DEPARTURE_STATION_KEY] == departure_city)
            & (df[ld.ARRIVAL_STATION_KEY] == arrival_city)
        ][ld.MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT].mean()
    )
