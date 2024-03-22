import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta


# function times (modified from https://codereview.stackexchange.com/a/274228)
def to_timedelta(t: time) -> timedelta:
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

def to_time(seconds: int) -> time:
    return (datetime.min + timedelta(seconds=seconds)).time()

def random_time(start_time: time, end_time: time) -> time:
    start = to_timedelta(start_time)
    end = to_timedelta(end_time)
    duration = (end - start).seconds
    random_offset = np.random.randint(0, duration)
    time = to_time((start + timedelta(seconds=random_offset)).seconds)
    return time.strftime("%H:%M")

def generate_random_transactions(num_days = 5,
                                 open_time = '08:00',
                                 close_time = '12:00',
                                 num_banks = 5,
                                 min_bal = 100,
                                 max_bal = 300,
                                 min_txn_count = 5,
                                 max_txn_count = 10,
                                 min_txn_value = 10,
                                 max_txn_value = 50,
                                 seed = 123,
                                ):
    np.random.seed(123)
    
    # generate banks
    banks = {'name': [f'b{i}' for i in range(1, num_banks+1)],
             'bank': [f'Bank {i}' for i in range(1, num_banks+1)]}
    banks = pd.DataFrame(banks)
    
    # generate accounts
    accounts = {'id': [f'acc{i}' for i in range(1, num_banks+1)],
                'owner': [f'b{i}' for i in range(1, num_banks+1)],
                'balance': [np.random.randint(min_bal, max_bal) for _ in range(1, num_banks+1)]}
    accounts = pd.DataFrame(accounts)
    
    # generate transactions
    transactions = []

    for day in range(1, num_days+1):
        for bank_1 in range(1, num_banks+1):
            for bank_2 in range(1, num_banks+1):
                if bank_1 == bank_2: continue
                num_txn = np.random.randint(min_txn_count, max_txn_count)
                for _ in range(num_txn):
                    amount = (max_txn_value-min_txn_value) * np.random.random() + min_txn_value
                    
                    transactions.append({
                        'day': day,
                        'time': random_time(time.fromisoformat(open_time),
                                            time.fromisoformat(close_time)),
                        'sender_account': 'acc'+str(bank_1),
                        'receipient_account': 'acc'+str(bank_2),
                        'amount': int(np.round(amount)),
                    })
                    
    transactions.sort(key=lambda x: (x['day'], x['time']))
    transactions = pd.DataFrame(transactions)

    return banks, accounts, transactions