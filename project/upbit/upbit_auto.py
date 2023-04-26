import pyupbit

# Set up the PyUpbit API client
access_key = "ujiEYhMy6XG8qPgxfEi0xenkaTcrYpGINkxv13Zk"
secret_key = "oAzFic1wlVU3KnUrDjriugkzRXElDyD9Dxf4S76m"
upbit = pyupbit.Upbit(access_key, secret_key)

# Set up the trading parameters
target_currency = "BTC"
buy_amount = 1000000  # Amount to buy in KRW
sell_amount = 0.01  # Amount to sell in BTC
profit_margin = 0.01  # Desired profit margin

# Start the trading loop
while True:
    # Get the current market price of the target currency
    market_price = pyupbit.get_current_price(f"KRW-{target_currency}")
    
    # Get the current balance of the target currency in the account
    currency_balance = upbit.get_balance(f"{target_currency}")
    
    # Check if we have enough KRW balance to buy the target currency
    krw_balance = upbit.get_balance("KRW")
    if krw_balance < buy_amount:
        print("Not enough KRW balance to buy.")
    else:
        # Calculate the amount of currency to buy
        buy_price = buy_amount / market_price
        print(f"Buying {buy_price} {target_currency} at {market_price} KRW.")
        
        # Place the buy order
        upbit.buy_market_order(f"KRW-{target_currency}", buy_amount)
        
        # Wait for the order to complete
        while upbit.get_order(target_currency)[0]['state'] != 'done':
            pass
        
        # Get the new balance of the target currency in the account
        currency_balance = upbit.get_balance(f"{target_currency}")
        print(f"New {target_currency} balance: {currency_balance}")
    
    # Check if we have enough currency balance to sell
    if currency_balance < sell_amount:
        print("Not enough currency balance to sell.")
    else:
        # Calculate the sell price based on the desired profit margin
        sell_price = market_price * (1 + profit_margin)
        print(f"Selling {sell_amount} {target_currency} at {sell_price} KRW.")
        
        # Place the sell order
        upbit.sell_market_order(f"KRW-{target_currency}", sell_amount)
        
        # Wait for the order to complete
        while upbit.get_order(target_currency)[0]['state'] != 'done':
            pass
        
        # Get the new balance of the target currency in the account
        currency_balance = upbit.get_balance(f"{target_currency}")
        print(f"New {target_currency} balance: {currency_balance}")
