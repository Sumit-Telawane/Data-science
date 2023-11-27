
import os
from art import *
import os

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def get_winner(bidders):
    winner_amt = 0
    winner_name = ''
    for key in bidders:
        if bidders[key] > winner_amt:
            winner_amt = bidders[key]
            winner_name = key
    print(f'The winner is {winner_name} with ${winner_amt}')

print(logo)
print('welcome to the silent auction')

more_bidders = True
bids = {}

while more_bidders:
    bidder_name = input("What is your name? ")
    bidder_bid = int(input("What is your bid? "))
    other_bidders = input("Are there any other bidders? Type 'yes' or 'no'.\n").lower()
    
    bids[bidder_name] = bidder_bid
    clear_terminal()
    if other_bidders == 'yes':
        continue
    else:
        more_bidders = False
        get_winner(bids)
    
