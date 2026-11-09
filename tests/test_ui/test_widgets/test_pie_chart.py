from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt
import pytest

from ui.widgets import pie_chart


def test_display_pie_chart():
    # Mock streamlit.pyplot to avoid rendering a real plot in tests
    with (
        patch("streamlit.pyplot") as mock_st_pyplot,
        patch("matplotlib.pyplot.gcf") as mock_gcf,
    ):
        mock_fig = MagicMock()
        mock_gcf.return_value = mock_fig

        cause_list = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0]

        # This should not raise any exceptions
        pie_chart.display_pie_chart(cause_list)

        mock_st_pyplot.assert_called_once_with(mock_fig)
