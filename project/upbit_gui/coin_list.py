import tkinter as tk
from upbit import coin_symbols

def chunked(seq, chunk_size):
    """seq를 chunk_size 개씩 끊어서 리스트로 반환하는 함수"""
    return [seq[i:i+chunk_size] for i in range(0, len(seq), chunk_size)]

def open_new_window():
    new_window = tk.Toplevel()
    new_window.title("New Window")
    new_window.geometry("400x300")
    return new_window
    
def coin_list_window():
    # 코인 심볼을 출력할 리스트박스 생성
    show_coin_list = open_new_window()
    coin_listbox = tk.Listbox(show_coin_list)
    coin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 코인 심볼을 리스트박스에 추가
    coin_chunks = chunked(coin_symbols, 5)
    for chunk in coin_chunks:
        coin_listbox.insert(tk.END, ", ".join(chunk))

    # 리스트박스에 스크롤바 연결
    scrollbar = tk.Scrollbar(show_coin_list, orient=tk.VERTICAL, command=coin_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    coin_listbox.configure(yscrollcommand=scrollbar.set)