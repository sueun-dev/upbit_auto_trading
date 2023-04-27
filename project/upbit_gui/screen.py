import tkinter as tk
import threading
from tkinter import scrolledtext
from upbit import update_text_box
from select_coin import add_coin, delete_coin
import coin_list

window = tk.Tk()
window.title("Crypto Price Tracker")

##########
#  RIGHT #
##########

right_frame = tk.Frame(window, bg="lightgreen", width=300, height=400)
right_frame.pack(side=tk.RIGHT, padx=5, pady=5, expand=True, fill=tk.BOTH)

# 오른쪽 프레임에 ScrolledText 추가 (right_frame1)
right_frame_up = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=20, height=8)
right_frame_up.pack(side=tk.TOP, padx=5, pady=5, expand=True, fill=tk.BOTH)  # side=tk.TOP 사용하여 상단에 배치

# 오른쪽 프레임에 ScrolledText 추가 (right_frame2)
right_frame_down = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=20, height=20)
right_frame_down.pack(side=tk.BOTTOM, padx=5, pady=5, expand=True, fill=tk.BOTH)  # side=tk.BOTTOM 사용하여 하단에 배치


##########
#  LEFT  #
##########
left_frame = tk.Frame(window, bg="lightblue", width=300, height=400)
left_frame.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.BOTH)

# Create a scrolled text box
text_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=70, height=20)
text_box.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

get_text_button = tk.Button(left_frame, text="Add trace coin", command=add_coin, font=("Helvetica", 10))
get_text_button.pack(padx=0, pady=0, side=tk.LEFT)

get_text_button = tk.Button(left_frame, text="Remove trace coin", command=delete_coin, font=("Helvetica", 10))
get_text_button.pack(padx=5, pady=0, side=tk.LEFT)

get_text_button = tk.Button(left_frame, text="coin list", command=coin_list.open_new_window, font=("Helvetica", 10))
get_text_button.pack(padx=5, pady=0, side=tk.LEFT)

# Add coin
entry_label = tk.Label(left_frame, text="add coin. write like -> btc, eth, sol, matic etc...")
entry_label.pack(padx=30, pady=0, side=tk.TOP, anchor=tk.W)
entry = tk.Entry(left_frame, width=30)
entry.pack(padx=10, pady=10, side=tk.LEFT)

# Start the update_text_box function in a separate thread
threading.Thread(target=update_text_box, daemon=True).start()

# Run the tkinter main loop
window.mainloop()
