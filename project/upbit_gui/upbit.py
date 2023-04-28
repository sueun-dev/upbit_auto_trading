import pyupbit
import time
import tkinter as tk
from tkinter import scrolledtext
import screen

coin_list_tickers = pyupbit.get_tickers(fiat="KRW")
coin_symbols = [ticker.replace("KRW-", "") for ticker in coin_list_tickers]

tickers = ["KRW-BTC", "KRW-ETH"]

clear_coin_trigger = False

# Function to update the text box
def update_text_box():
    new_trace_coin()
    while True:
        screen.get_add_coin_button.config(state=tk.DISABLED)
        screen.get_remove_coin_button.config(state=tk.DISABLED)
        prices = pyupbit.get_current_price(tickers)
        biggest_gainer = None
        biggest_gainer_pct = 0
        biggest_loser = None
        biggest_loser_pct = 0

        screen.coin_price_box.config(state=tk.NORMAL)

        for ticker in tickers:
            try:
                df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
                if df is not None:
                    start_price = df["close"].iloc[0]
                    end_price = df["close"].iloc[-1]
                    pct_change = (end_price - start_price) / start_price * 100

                    output = f"{ticker}: {prices[ticker]:.2f} ({pct_change:.2f}%)"
                    screen.coin_price_box.insert(tk.END, output + "\n")

                    if pct_change > biggest_gainer_pct:
                        biggest_gainer = ticker
                        biggest_gainer_pct = pct_change
                    if pct_change < biggest_loser_pct:
                        biggest_loser = ticker
                        biggest_loser_pct = pct_change
            except pyupbit.UpbitError:
                print('wait!')
                time.sleep(10)
                continue

        coin_price_box(biggest_gainer, biggest_gainer_pct, biggest_loser, biggest_loser_pct)
        screen.get_add_coin_button.config(state=tk.NORMAL)
        screen.get_remove_coin_button.config(state=tk.NORMAL)
        time.sleep(5)

def new_trace_coin():
    screen.right_frame_up.delete("1.0", "end")
    screen.right_frame_up.insert(tk.END, tickers)
    
def clear_coin_board():
    screen.coin_price_box.config(state=tk.NORMAL)
    screen.coin_price_box.delete("1.0", "end")

#그리고 텍스트 위젯은 이렇게 텍스트의 삽입 혹은 수정을 허용하는 게 기본값이기 때문에 이걸 못하게 
#.config()로 속성을 지정할 수 있다. 기본값 state='normal'을 state='disabled'로 설정하면 수정이 불가하다.
def coin_price_box(biggest_gainer, biggest_gainer_pct, biggest_loser, biggest_loser_pct):
    screen.coin_price_box.insert(tk.END, f"\nBiggest gainer: {biggest_gainer} ({biggest_gainer_pct:.2f}%)\n")
    screen.coin_price_box.insert(tk.END, f"Biggest loser: {biggest_loser} ({biggest_loser_pct:.2f}%)\n")
    screen.coin_price_box.insert(tk.END, "-------------------------\n")
    screen.coin_price_box.see(tk.END)
    screen.coin_price_box.update_idletasks()
    screen.coin_price_box.config(state=tk.DISABLED)
    