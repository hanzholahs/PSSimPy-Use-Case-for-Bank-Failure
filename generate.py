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


# settings
num_days = 10
open_time = '08:00'
close_time = '17:00'
num_banks = 7
n_day_txn_per_bank = 25
min_value = 25
max_value = 75


# generate transactions
transactions = []

for day in range(1, num_days+1):
    for bank_1 in range(1, num_banks+1):
        for bank_2 in range(1, num_banks+1):
            if bank_1 == bank_2: continue
            for _ in range(n_day_txn_per_bank):
                amount = (max_value-min_value) * np.random.random() + min_value
                
                transactions.append({
                    'day': day,
                    'time': random_time(time.fromisoformat(open_time),
                                        time.fromisoformat(close_time)),
                    'sender_account': 'acc'+str(bank_1),
                    'receipient_account': 'acc'+str(bank_2),
                    'amount': int(np.round(amount)),
                })


# export results      
transactions = pd.DataFrame(transactions).sort_values(['day', 'time'])
transactions.to_csv('data/random_transactions.csv', index=False)