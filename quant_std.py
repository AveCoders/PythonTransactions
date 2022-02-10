
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain, groupby
import csv
from csv import DictReader
from re import A
import statistics as mean
import pprint
from prometheus_client import Counter

from pyrsistent import v 

pp = pprint.PrettyPrinter(indent=3)

@dataclass
class Transaction:
    transactionId: str
    accountId: str
    transactionDay: int
    category: str
    transactionAmount: float 

file_path = 'transactions.txt'

transactions = []


def create_transactionDB() :

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',') # read the file
        next(csv_reader) # skip the header
        
        for row in csv_reader:
            transaction = Transaction(row[0], row[1], int(row[2]), row[3], float(row[4])) # build an object              
            transactions.append(transaction)            

    return transactions


trans = create_transactionDB()

days = set()

for trans_days in trans:
    days.add(trans_days.transactionDay)


def daytrade_ops(trans):
        
    """
    Calculates the total transaciton value for all transactions for each day
    TODO: make range cap dynamic
    """
       
    for i in range (trans[0].transactionDay, len(days)+1): 
       day_amount = (sum([day.transactionAmount for day in trans if day.transactionDay == i]))
       print(f' Day {i} brought {day_amount:.2f}')



def trans_type(trans):
    """
    Calculates the average value of transactions per account for each type of transaction
    Acc ID: blabla AA = avg(56574)
    Does it means average of each type of transactions grouped or provided for each accound ID?
    Take accountId, take category, calculate average 
    for accId in trans
    """
    
    sorted_trans = sorted(trans, key=lambda x: (x.accountId, x.category)) # need to sort transactions or groupby won't work correctly (duplicates)

    for k, g in groupby(sorted_trans, lambda x: (x.accountId, x.category)): #  # maybe not required

            
            cat_trans = [x.transactionAmount for x in g ]
            total_trans = sum(cat_trans)
            avg_val = total_trans / len(cat_trans)
            
            
            print(f'AccountId: {k[0]}, transaction type {k[1]}, average value per transaction {avg_val:.2F}')
                
d = defaultdict(float)

def totals_per_cat(transactions):
    
    for accountId, transactionAmount in chain.from_iterable(transactions):
                 d[accountId] += transactionAmount
    trans_res = list(d.values())
    return trans_res
    
def unique_keys(transactions):
    for accountId, transactionAmount in chain.from_iterable(transactions):
                d[accountId] += transactionAmount
    unique_keys = list(d.keys()) 
    return unique_keys


def rolling_window(trans, window_size, day):
    sorted_trans = sorted(trans, key=lambda x: (x.accountId, x.category))
    
    # the base length check
    if day <= window_size:
        return trans
    #for each day

    # maybe not required
   # for i in range (day-1, day-window_size-1, -1): 

        for k, g in groupby(sorted_trans, lambda x: (x.accountId, x.category) ): # groups them by account Id and category
            
            cat_trans = [x.transactionAmount for x in g ] # extracts transaction values
            day_amount = max(cat_trans) # maximum transaction value for the Accound Id and Category/Type
            total_trans = sum(cat_trans) # total transaction value for Account Id and Category/Tupe
            avg_val = total_trans / len(cat_trans) # average transaction value for Account Id and Category/Tupe
            
            print(f'Day: {i} Account ID: {k[0]} Category/Type: {k[1]} Maximum: {day_amount} Average: {avg_val:.2F} Total: {total_trans:.2F}')
        
    for i in range(day-window_size, day): 
        
        total_trans = []

        trans_AA = []
        trans_CC = []
        trans_FF = []

        total_trans.append([(x.accountId, x.transactionAmount) for x in sorted_trans])

        #proba = ([(x.accountId, x.transactionAmount) for x in sorted_trans])
        
        trans_AA.append([(x.accountId, x.transactionAmount) for x in sorted_trans  if x.category == "AA"])
        trans_CC.append([(x.accountId, x.transactionAmount) for x in sorted_trans  if x.category == "CC"])
        trans_FF.append([(x.accountId, x.transactionAmount) for x in sorted_trans  if x.category == "FF"])

        

        #TODO: return average transactionAmount per account for the last 5 days

        #TODO: return maximum transactionAmount per account for the last 5 days
        
        for el in range(0, len(trans_AA)):
                print(f'''Day {i}  Account ID    {unique_keys(trans_AA)[el]}    Maximum  "Placeholder"   Average   "Placeholder"   AA total value {totals_per_cat(trans_AA)[el]} CC total value {totals_per_cat(trans_CC)[el]} FF total value {totals_per_cat(trans_FF)[el]}  ''')
                el +=1    
      
#daytrade_ops(trans)

#trans_type(trans)
rolling_window(trans, 5, 10)

