import pandas as pd
from plotly.graph_objs import Figure
from src.utils.plots import plot_stock_chart_line
from unittest.mock import patch


def test_plot_stock_chart_line_returns_figure():
    # Sample data
    df = pd.DataFrame({
        'Date': pd.date_range('2025-08-01', periods=5),
        'Close': [100, 102, 101, 99, 98]
    })
    # Don't set index—keep 'Date' as a column


    # Mock yfinance.Ticker.info
    with patch('yfinance.Ticker') as MockTicker:
        MockTicker.return_value.info = {
            'currency': 'USD',
            'displayName': 'Apple Inc.'
        }

        fig = plot_stock_chart_line(df, 'AAPL')

        assert isinstance(fig, Figure)
        assert fig.layout.title.text == 'Chart of the Apple Inc. Stock'
        assert fig.data[0].y.tolist() == [100, 102, 101, 99, 98]
