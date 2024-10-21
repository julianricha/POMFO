### POMFO - Portfolio Optimization for Multi-Family Office

This Python application is a web-based portfolio optimization tool developed using the Dash framework and Plotly for data visualization. The app allows users to input their personal financial details and generates a recommended portfolio allocation based on their determined risk tolerance. Additionally, it displays key metrics such as the expected annual return, portfolio volatility, and the Sharpe ratio, utilizing real-time financial data fetched from Yahoo Finance through the YFinance API.

#### Key Features:
1. **User Input Fields**:
   The app collects user inputs such as: Age, Net Worth, Number of Dependents
   These inputs help determine the user's risk tolerance (Aggressive, Balanced, or Conservative).

2. **Risk Tolerance and Portfolio Allocation**:
   - Based on the user's inputs, the app calculates the user's risk tolerance:
     - **Aggressive**: High allocation to stocks.
     - **Balanced**: Moderate allocation to stocks and bonds.
     - **Conservative**: Higher allocation to bonds and cash.
   - The app then generates a corresponding portfolio allocation across four asset classes:
     - **Stocks, Bonds, Real Estate, Cash**

3. **Data Fetching with YFinance**:
   - The app uses the **yfinance** library to fetch historical stock market data for the selected asset classes
   - Used ETFs as proxys for simplicity: SPY for stocks, TLT for bonds, RSPR for real estate.
   - The fetched data is used to calculate the **expected return** and **volatility** for each asset class.

4. **Portfolio Metrics Calculation**:
   - **Expected Annual Return**: The weighted average of expected returns across the allocated assets.
   - **Portfolio Volatility**: Calculated using the weighted standard deviations of each asset class.
   - **Sharpe Ratio**: Measures the risk-adjusted return by comparing excess portfolio return to its volatility.

5. **Pie Chart Visualization**:
   - A pie chart is generated using **Plotly** to visualize the portfolio allocation across the asset classes.

6. **Metrics Output**:
   - The calculated **Annual Return**, **Portfolio Volatility**, and **Sharpe Ratio** are displayed beneath the pie chart for easy reference.

7. **Progress Bar Suppression**:
   - The **progress bars** from yfinance are suppressed using Python’s `contextlib.redirect_stdout()` to avoid cluttering the output when fetching financial data.

#### How the App Works:
- Users input their age, income, and number of dependents.
- When the "Optimize Portfolio" button is clicked, the app:
   - Determines the user's risk tolerance.
   - Allocates the portfolio based on the risk tolerance.
   - Fetches historical data to calculate the portfolio's expected return, volatility, and Sharpe ratio.
   - Displays the portfolio allocation in a pie chart.
   - Outputs the portfolio’s key metrics (expected return, volatility, and Sharpe ratio).

This app provides a simple yet powerful way for users to understand their optimal portfolio allocation based on personal financial details, giving them a clearer picture of their potential investment returns and risks.
