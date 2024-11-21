import pandas as pd
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt

# Enable interactive mode
matplotlib.use('TkAgg')

# Download historical data
data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Calculate moving averages
data['Fast_MA'] = data['Close'].rolling(window=10).mean()
data['Slow_MA'] = data['Close'].rolling(window=50).mean()

# Define signals
data['Signal'] = 0
data.loc[data['Fast_MA'] > data['Slow_MA'], 'Signal'] = 1  # Buy signal
data.loc[data['Fast_MA'] <= data['Slow_MA'], 'Signal'] = -1  # Sell signal

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Fast_MA'], label='Fast MA (10)', linestyle='--')
plt.plot(data['Slow_MA'], label='Slow MA (50)', linestyle='--')
plt.legend()
plt.title('Moving Average Crossover Strategy')
plt.show()
