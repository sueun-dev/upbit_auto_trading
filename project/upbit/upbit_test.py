import pyupbit
import time
# ready
# Get all KRW trading pairs
tickers = pyupbit.get_tickers(fiat="KRW")

tickers = [ticker for ticker in tickers if ticker != "KRW-BTT"]

# Loop indefinitely to get live prices every 10 seconds
while True:
    # Get the current prices for all tickers
    prices = pyupbit.get_current_price(tickers)

    biggest_gainer = None
    biggest_gainer_pct = 0
    biggest_loser = None
    biggest_loser_pct = 0

    # Loop through the tickers and print their current price and 30-second percentage change
    for ticker in tickers:
        # Get the OHLCV data for the ticker for the last 2 minutes
        df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
        # Check if df is None before trying to access its columns
        if df is not None:
            # Calculate the percentage change in price compared to 30 seconds ago
            start_price = df["close"].iloc[0]
            end_price = df["close"].iloc[-1]
            pct_change = (end_price - start_price) / start_price * 100
            # Print the current price and percentage change
            print(f"{ticker}: {prices[ticker]:.2f} ({pct_change:.2f}%)")

            if pct_change > biggest_gainer_pct:
                biggest_gainer = ticker
                biggest_gainer_pct = pct_change
            if pct_change < biggest_loser_pct:
                biggest_loser = ticker
                biggest_loser_pct = pct_change

    print(f"\nBiggest gainer: {biggest_gainer} ({biggest_gainer_pct:.2f}%)")
    print(f"Biggest loser: {biggest_loser} ({biggest_loser_pct:.2f}%)\n")
    print("-------------------------")
    # Wait for 30 seconds before getting the prices again
    time.sleep(30)
