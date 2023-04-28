import screen
from upbit import tickers, new_trace_coin, coin_list_tickers


def add_coin():
    entry_text = "KRW-" + screen.entry.get().upper()
    found = False

    for i in range(len(tickers)):
        if entry_text == tickers[i]:
            found = True
            print("You already have this coin")
            break
        elif entry_text == "KRW-":
            found = True
            print("NULL")
            break
    if not found:
        if entry_text in coin_list_tickers:
            print("Coin is available")
            tickers.append(entry_text)
            new_trace_coin()
        else:
            print("Coin is not available")
            found = True


def delete_coin():
    if len(tickers) > 2 :
        entry_text = "KRW-" + screen.entry.get().upper()
        for i, coin in enumerate(tickers):
            if entry_text == coin:
                tickers.pop(i)
                new_trace_coin()
                break
    else :
        print("need more coin to compare it")
    