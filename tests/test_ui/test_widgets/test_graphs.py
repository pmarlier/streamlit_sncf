from unittest.mock import patch

import pandas as pd
import pytest

from ui.widgets import graphs


def test_monthly_arrival_delay_distribution_graph_display_without_data(
    mocked_delay_df,
) -> None:
    """Test the display of the Monthly arrival delay distibution graph
    when no delay data is available."""

    with (
        patch("core.load_data.df", mocked_delay_df, create=True),
        patch("streamlit.info") as mocked_streamlit_info,
        patch("streamlit.plotly_chart") as mocked_streamlit_plotly_chart,
    ):
        graphs.display_monthly_arrival_delay_graph(
            "RENNES",
            "PARIS MONTPARNASSE",
            1,
            12,
            [2022, 2023],
            actual_year=2026,
        )

        # check the displayed message
        mocked_streamlit_info.assert_called_once_with(
            "Aucune donnée disponible pour la période sélectionnée."
        )

        # check that there is no graph
        mocked_streamlit_plotly_chart.assert_not_called()


def test_monthly_arrival_delay_distribution_graph_display_with_data(
    mocked_delay_df,
) -> None:
    """Test the display of the Monthly arrival delay distibution graph
    when there is data."""

    with (
        patch("core.load_data.df", mocked_delay_df, create=True),
        patch("streamlit.info") as mocked_streamlit_info,
        patch("streamlit.plotly_chart") as mocked_streamlit_plotly_chart,
    ):
        graphs.display_monthly_arrival_delay_graph(
            "PARIS MONTPARNASSE",
            "RENNES",
            1,
            2,
            [2019, 2022, 2023, 2026],
            actual_year=2026,
        )

        # check that no message is displayed
        mocked_streamlit_info.assert_not_called()

        # check that the graph is displayed
        mocked_streamlit_plotly_chart.assert_called_once()

        # get the graph passed to streamlit
        graph = mocked_streamlit_plotly_chart.call_args.args[0]

        # verify the number of curves
        assert len(graph.data) == 4


def test_monthly_arrival_delay_distribution_graph_curves(
    mocked_delay_df,
) -> None:
    """Test the values of the historical curve, the actual year
    curve as well as the highlighted curves."""

    with (
        patch("core.load_data.df", mocked_delay_df, create=True),
        patch("streamlit.plotly_chart") as mocked_streamlit_plotly_chart,
    ):
        graphs.display_monthly_arrival_delay_graph(
            "PARIS MONTPARNASSE",
            "RENNES",
            1,
            1,
            [2019, 2022, 2023, 2026],
            actual_year=2026,
        )

        graph = mocked_streamlit_plotly_chart.call_args.args[0]

        # get the curves
        historical_curve = graph.data[0]
        actual_year_curve = graph.data[1]
        highlighted_historical_curve = graph.data[2]
        highlighted_actual_year_curve = graph.data[3]

        # check the previous years' (historical) curve
        # and then the actual year curve
        assert historical_curve.y[0] == 30.0
        assert historical_curve.y[1] == 26.3
        assert actual_year_curve.y[0] == 35.0
        assert pd.isna(actual_year_curve.y[1])

        # check the highlighted curves
        assert highlighted_historical_curve.y[0] == 30.0
        assert pd.isna(highlighted_historical_curve.y[1])
        assert highlighted_actual_year_curve.y[0] == 35.0
        assert pd.isna(highlighted_actual_year_curve.y[1])


def test_monthly_arrival_delay_distribution_graph_colored_zones(
    mocked_delay_df,
) -> None:
    """Test the minimum-maximum and the Q1-Q3 zones
    for the selected previous years' data"""

    with (
        patch("core.load_data.df", mocked_delay_df, create=True),
        patch("streamlit.plotly_chart") as mocked_streamlit_plotly_chart,
    ):
        graphs.display_monthly_arrival_delay_graph(
            "PARIS MONTPARNASSE",
            "RENNES",
            1,
            1,
            [2018, 2019, 2020, 2022, 2023, 2026],
            actual_year=2026,
        )

        graph = mocked_streamlit_plotly_chart.call_args.args[0]

        # check the number of colored zones
        assert len(graph.layout.shapes) == 3
        min_max_zone = graph.layout.shapes[0]
        quartile_zone = graph.layout.shapes[1]
        # get the zone for unselected month:
        unselected_min_max_zone = graph.layout.shapes[2]

        # check the minimum-maximum zones
        assert min_max_zone.type == "rect"
        assert min_max_zone.x0 == 0.5
        assert min_max_zone.x1 == 1.5
        assert min_max_zone.y0 == 20.1
        assert min_max_zone.y1 == 40.0
        assert min_max_zone.fillcolor == "rgba(245, 158, 11, 0.18)"
        assert min_max_zone.layer == "below"

        # check the Q1-Q3 zones
        assert quartile_zone.type == "rect"
        assert quartile_zone.x0 == 0.5
        assert quartile_zone.x1 == 1.5
        assert quartile_zone.y0 == pytest.approx(21.10280374)
        assert quartile_zone.y1 == 30.0
        assert quartile_zone.fillcolor == "rgba(245, 158, 11, 0.35)"
        assert quartile_zone.layer == "below"

        # check the minimum-maximum zone for an unselected month
        assert unselected_min_max_zone.type == "rect"
        assert unselected_min_max_zone.x0 == 1.5
        assert unselected_min_max_zone.x1 == 2.5
        assert unselected_min_max_zone.y0 == 26.3
        assert unselected_min_max_zone.y1 == 34.35
        assert unselected_min_max_zone.fillcolor == "rgba(100, 116, 139, 0.15)"
        assert unselected_min_max_zone.layer == "below"


def test_monthly_arrival_delay_distribution_graph_tooltips(
    mocked_delay_df,
) -> None:
    """Test the information displayed in the tooltips."""

    with (
        patch("core.load_data.df", mocked_delay_df, create=True),
        patch("streamlit.plotly_chart") as mocked_streamlit_plotly_chart,
    ):
        graphs.display_monthly_arrival_delay_graph(
            "PARIS MONTPARNASSE",
            "RENNES",
            1,
            2,
            [2019, 2022, 2023, 2026],
            actual_year=2026,
        )

        graph = mocked_streamlit_plotly_chart.call_args.args[0]

        historical_curve = graph.data[0]
        actual_year_curve = graph.data[1]

        # check the previous years' number of observations
        assert historical_curve.customdata[0][0] == 3
        assert historical_curve.customdata[1][0] == 1
        assert historical_curve.customdata[2][0] == 0

        # check the previous years' number of delayed trains
        assert historical_curve.customdata[0][1] == 316
        assert historical_curve.customdata[1][1] == 112
        assert historical_curve.customdata[2][1] == "Non renseigné"

        # check the actual year number of delayed trains
        assert actual_year_curve.customdata[0][0] == 110
        assert actual_year_curve.customdata[1][0] == "Non renseigné"
