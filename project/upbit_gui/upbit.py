import pyupbit
import time
import tkinter as tk
from tkinter import scrolledtext
import screen

tickers = ["KRW-BTC", "KRW-ETH"]

# Function to update the text box
def update_text_box():
    check_trace_coin()
    while True:
        prices = pyupbit.get_current_price(tickers)
        biggest_gainer = None
        biggest_gainer_pct = 0
        biggest_loser = None
        biggest_loser_pct = 0

        screen.text_box.config(state=tk.NORMAL)

        for ticker in tickers:
            df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
            if df is not None:
                start_price = df["close"].iloc[0]
                end_price = df["close"].iloc[-1]
                pct_change = (end_price - start_price) / start_price * 100

                output = f"{ticker}: {prices[ticker]:.2f} ({pct_change:.2f}%)"
                screen.text_box.insert(tk.END, output + "\n")

                if pct_change > biggest_gainer_pct:
                    biggest_gainer = ticker
                    biggest_gainer_pct = pct_change
                if pct_change < biggest_loser_pct:
                    biggest_loser = ticker
                    biggest_loser_pct = pct_change

        screen.text_box.insert(tk.END, f"\nBiggest gainer: {biggest_gainer} ({biggest_gainer_pct:.2f}%)\n")
        screen.text_box.insert(tk.END, f"Biggest loser: {biggest_loser} ({biggest_loser_pct:.2f}%)\n")
        screen.text_box.insert(tk.END, "-------------------------\n")
        screen.text_box.see(tk.END)
        screen.text_box.update_idletasks()
        screen.text_box.config(state=tk.DISABLED)
        
        time.sleep(2)

def check_trace_coin():
    screen.right_frame_up.delete("1.0", "end")
    screen.right_frame_up.insert(tk.END, tickers)