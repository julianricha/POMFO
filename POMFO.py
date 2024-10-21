import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import contextlib
import sys

# Step 3: Asset Allocation
def asset_allocation(risk_tolerance):
    """
    Returns asset allocation based on the user's risk tolerance.
    """
    if risk_tolerance == "Aggressive":
        return {"Stocks": 0.6, "Bonds": 0.3, "Real Estate": 0.05, "Cash": 0.05}
    elif risk_tolerance == "Balanced":
        return {"Stocks": 0.3, "Bonds": 0.4, "Real Estate": 0.15, "Cash": 0.05}
    else:
        return {"Stocks": 0.1, "Bonds": 0.5, "Real Estate": 0.3, "Cash": 0.1}

# Step 4: Fetch Historical Data using yfinance
def get_asset_data(ticker):
    """
    Fetches historical price data from Yahoo Finance using the yfinance library.
    Returns daily returns for the given ticker.
    """
    # Suppress output by redirecting stdout to null
    with contextlib.redirect_stdout(sys.stderr):
        data = yf.download(ticker, period="1y")
    data['Returns'] = data['Adj Close'].pct_change()  # Calculate daily returns
    return data['Returns'].dropna()

# Step 5: Calculate Expected Return and Volatility
def get_expected_return_and_volatility(ticker):
    """
    Calculates the expected return (mean) and volatility (std dev) for a given asset.
    """
    returns = get_asset_data(ticker)
    expected_return = returns.mean() * 252  # Annualized return
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    return expected_return, volatility

# Step 6: Get Expected Return and Volatility for the Portfolio
def portfolio_expected_return_and_volatility(asset_allocation):
    """
    Calculate the expected return and volatility for the portfolio
    using real data from yfinance and hardcoded values for cash.
    """
    tickers = {
        "Stocks": "SPY",         # S&P 500 ETF as a proxy for stocks
        "Bonds": "TLT",          # iShares 20+ Year Treasury Bond ETF as a proxy for bonds
        "Real Estate": "RSPR"    # Invesco Active US Real Estate ETF as a proxy for real estate
    }
    
    portfolio_return = 0
    portfolio_volatility = 0
    
    for asset, weight in asset_allocation.items():
        if asset == "Cash":
            # Hardcoded values for cash (2% return, 1% volatility)
            expected_return = 0.02
            volatility = 0.01
        else:
            # Fetch expected return and volatility for the asset class
            ticker = tickers[asset]
            expected_return, volatility = get_expected_return_and_volatility(ticker)
        
        portfolio_return += weight * expected_return
        portfolio_volatility += (weight * volatility) ** 2  # Variance

    portfolio_volatility = np.sqrt(portfolio_volatility)  # Standard deviation (volatility)
    
    return portfolio_return, portfolio_volatility

# Step 7: Calculate Sharpe Ratio
def sharpe_ratio(portfolio_return, portfolio_volatility, risk_free_rate=0.02):
    """
    Calculates the Sharpe Ratio of the portfolio.
    """
    excess_return = portfolio_return - risk_free_rate
    return excess_return / portfolio_volatility

# Step 8: Create the Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Portfolio Optimizer"),
    
    # Input fields for user data
    html.Div([
        html.Label("Enter Your Age: "),
        dcc.Input(id='input-age', type='number', value=30),
    ]),
    html.Div([
        html.Label("Enter Your Net Worth: "),
        dcc.Input(id='input-net-worth', type='number', value=500000),
    ]),
    html.Div([
        html.Label("Enter Number of Dependents: "),
        dcc.Input(id='input-dependents', type='number', value=0),
    ]),
    
    html.Button('Optimize Portfolio', id='submit-button', n_clicks=0),
    
    # Placeholder for pie chart
    dcc.Graph(id='pie-chart'),

    # Placeholder for portfolio metrics
    html.Div(id='metrics-output', style={'margin-top': '20px', 'font-size': '18px'}),
])

# Callback to update the pie chart and show metrics
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('metrics-output', 'children')],
    Input('submit-button', 'n_clicks'),
    State('input-age', 'value'),
    State('input-net-worth', 'value'),
    State('input-dependents', 'value'),
)
def update_pie_chart(n_clicks, age, net_worth, dependents):
    if n_clicks > 0:
        # Step 2: Determine risk tolerance based on user inputs
        if age < 35 and net_worth > 500000 and dependents == 0:
            risk_tolerance = "Aggressive"
        elif 35 <= age < 50 and net_worth > 250000:
            risk_tolerance = "Balanced"
        else:
            risk_tolerance = "Conservative"
        
        # Get the portfolio allocation based on risk tolerance
        allocation = asset_allocation(risk_tolerance)
        
        # Calculate portfolio expected return and volatility
        portfolio_return, portfolio_volatility = portfolio_expected_return_and_volatility(allocation)
        
        # Calculate Sharpe Ratio
        sharpe = sharpe_ratio(portfolio_return, portfolio_volatility)
        
        # Generate Pie Chart
        labels = list(allocation.keys())
        values = list(allocation.values())
        
        pie_chart_figure = go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=0.3)],
            layout=go.Layout(title=f'Portfolio Allocation ({risk_tolerance} Risk Tolerance)')
        )
        
        # Display Portfolio Metrics
        metrics_text = html.Div([
            html.Div(f"Annual Expected Portfolio Return: {portfolio_return:.2%}"),
            html.Div(f"Portfolio Volatility: {portfolio_volatility:.2%}"),
            html.Div(f"Sharpe Ratio: {sharpe:.2f}")
        ])
        
        return pie_chart_figure, metrics_text
    
    # Empty chart and metrics for initial load
    return go.Figure(), ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
