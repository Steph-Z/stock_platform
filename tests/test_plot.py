import pandas as pd
from plotly.graph_objs import Figure
from src.utils.plots import plot_stock_chart
from unittest.mock import patch


def test_plot_stock_chart_line_returns_figure():
    # Sample data
    df = pd.DataFrame({
        'Date': pd.date_range('2025-08-01', periods=5),
        'Close': [100, 102, 101, 99, 98]
    })
    comp_name = 'Apple' #is passed from main app usually, always will be there 
    #cause we catch wrong tickers/isins earlier
    
    #fake metadata 
    metadata = {'currency': 'USD'}

    fig = plot_stock_chart(df, comp_name, 'AAPL', chart_type= 'line', metadata= metadata )

    assert isinstance(fig, Figure)
    assert fig.data[0].y.tolist() == [100, 102, 101, 99, 98]
