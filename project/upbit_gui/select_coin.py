import screen
from upbit import tickers, check_trace_coin

def add_coin():
    entry_text = "KRW-" + screen.entry.get().upper()
    found = False

    for i in range(len(tickers)):
        if entry_text == tickers[i]:
            found = True
            print("You already have this coin")
            break

    if not found:
        tickers.append(entry_text)
        check_trace_coin()


def delete_coin():
    if len(tickers) > 2 :
        entry_text = "KRW-" + screen.entry.get().upper()
        for i, coin in enumerate(tickers):
            if entry_text == coin:
                tickers.pop(i)
                check_trace_coin()
                break
    else :
        print("need more coin to compare it")
    