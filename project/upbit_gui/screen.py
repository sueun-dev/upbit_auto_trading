#순서는 frame을 읽어오는 순서입니다. 만약 right 프레임을 먼저 하고 under 프레임을 잡으면 right 안에 under 가 들어갑니다.
import tkinter as tk
import threading
import coin_list
from tkinter import scrolledtext
from upbit import update_text_box, clear_coin_board
from select_coin import add_coin, delete_coin

############
#  WINDOW  #
############

window = tk.Tk()
window.title("Crypto Price Tracker")


###########
#  UNDER  #
###########

under_frame = tk.Frame(window, width=300, height=30)
under_frame.pack(side=tk.BOTTOM, padx=5, pady=5, expand=True, fill=tk.BOTH, anchor='s')

get_add_coin_button = tk.Button(under_frame, text="Add trace coin", command=add_coin, font=("Helvetica", 10), state=tk.DISABLED)
get_add_coin_button.pack(padx=0, pady=0, side=tk.LEFT)

get_remove_coin_button = tk.Button(under_frame, text="Remove trace coin", command=delete_coin, font=("Helvetica", 10), state=tk.DISABLED)
get_remove_coin_button.pack(padx=0, pady=0, side=tk.LEFT)

get_coin_list_button = tk.Button(under_frame, text="coin list", command=coin_list.coin_list_window, font=("Helvetica", 10))
get_coin_list_button.pack(padx=0, pady=0, side=tk.LEFT)

clear_coin_list_button = tk.Button(under_frame, text="clear board", command=clear_coin_board, font=("Helvetica", 10))
clear_coin_list_button.pack(padx=0, pady=0, side=tk.LEFT)


###########
#  RIGHT  #
###########

right_frame = tk.Frame(window, bg="lightgreen", width=300, height=400)
right_frame.pack(side=tk.RIGHT, padx=2, pady=2, expand=True, fill=tk.BOTH)

# 오른쪽 프레임에 ScrolledText 추가 (right_frame1)
right_frame_up = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=20, height=8)
right_frame_up.pack(side=tk.TOP, padx=2, pady=2, expand=True, fill=tk.BOTH)  # side=tk.TOP 사용하여 상단에 배치

# 오른쪽 프레임에 ScrolledText 추가 (right_frame2)
right_frame_down = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=20, height=20)
right_frame_down.pack(side=tk.BOTTOM, padx=2, pady=2, expand=True, fill=tk.BOTH)  # side=tk.BOTTOM 사용하여 하단에 배치

##########
#  LEFT  #
##########
left_frame = tk.Frame(window, bg="lightblue", width=300, height=400)
left_frame.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.BOTH)

# Create a scrolled text box
coin_price_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=100, height=20)
coin_price_box.pack(padx=2, pady=2, expand=True, fill=tk.BOTH)

# Add coin
entry_label = tk.Label(left_frame, text="add coin. write like -> btc, eth, sol, matic etc...", bg="lightblue")
entry_label.pack(padx=0, pady=0, side=tk.TOP, anchor=tk.W)
entry = tk.Entry(left_frame, width=30)
entry.pack(padx=3, pady=3, side=tk.LEFT)

# Start the update_text_box function in a separate thread
threading.Thread(target=update_text_box, daemon=True).start()

# Run the tkinter main loop
window.mainloop()
