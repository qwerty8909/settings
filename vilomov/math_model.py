import random

# Set the initial probabilities of each event
prob_a_win = 0.4
prob_b_win = 0.3
prob_no_win = 0.3

# Set the initial odds for each event
odds_a_win = 1/prob_a_win
odds_b_win = 1/prob_b_win
odds_no_win = 1/prob_no_win

# Set the initial bank balance
bank_balance = 1000000

# Function to calculate the new odds based on the current bets
def adjust_odds(bets_a_win, bets_b_win, bets_no_win):
    total_bets = bets_a_win + bets_b_win + bets_no_win

    # Calculate the new probabilities based on the current bets
    new_prob_a_win = (bets_a_win/total_bets) * 0.5 + 0.25
    new_prob_b_win = (bets_b_win/total_bets) * 0.5 + 0.25
    new_prob_no_win = (bets_no_win/total_bets) * 0.5 + 0.25

    # Calculate the new odds based on the new probabilities
    new_odds_a_win = 1/new_prob_a_win
    new_odds_b_win = 1/new_prob_b_win
    new_odds_no_win = 1/new_prob_no_win

    return new_odds_a_win, new_odds_b_win, new_odds_no_win

# Function to simulate a single game and calculate the payout
def play_game(bets_a_win, bets_b_win, bets_no_win):
    global bank_balance

    # Randomly select the winning team or no win
    rand = random.random()
    if rand < prob_a_win:
        winner = 'a'
    elif rand < prob_a_win + prob_b_win:
        winner = 'b'
    else:
        winner = 'no'

    # Calculate the payout for each bet
    if winner == 'a':
        payout_a_win = bets_a_win * odds_a_win
        payout_b_win = 0
        payout_no_win = bets_no_win * odds_no_win
    elif winner == 'b':
        payout_a_win = 0
        payout_b_win = bets_b_win * odds_b_win
        payout_no_win = bets_no_win * odds_no_win
    else:
        payout_a_win = 0
        payout_b_win = 0
        payout_no_win = bets_no_win * odds_no_win

    # Update the bank balance
    bank_balance -= payout_a_win + payout_b_win + payout_no_win

    # Return the payout for each bet
    return payout_a_win, payout_b_win, payout_no_win

# Main loop
while True:
    # Get the current bets from the user
    bets_a_win = int(input("Введите сумму ставок на победу команды А: "))
    bets_b_win = int(input("Введите сумму ставок на победу команды Б: "))
    bets_no_win = int(input("Введите сумму ставок на НИЧЬЮ: "))

    # Adjust the odds based on the current bets
    odds_a_win, odds_b_win, odds_no_win = adjust_odds(bets_a_win, bets_b_win, bets_no_win)

    # Display the current odds to the user
    print("Current odds:")
    print("Team a to win: 1/{:.2f}".format(odds_a_win))
    print("Team b to win: 1/{:.2f}".format(odds_b_win))
    print("No win: {:.2f}".format(odds_no_win))

    # Simulate the game and calculate the payout for each bet
    payout_a_win, payout_b_win, payout_no_win = play_game(bets_a_win, bets_b_win, bets_no_win)

    # Display the payout for each bet to the user
    print("Payouts:")
    print("Team a to win: {:.2f}".format(payout_a_win))
    print("Team b to win: {:.2f}".format(payout_b_win))
    print("No win: {:.2f}".format(payout_no_win))

    # Check if the bank is bankrupt
    if bank_balance <= 0:
        print("The bank is bankrupt! Game over.")
    break

    # Ask the user if they want to continue playing
    answer = input("Do you want to continue playing? (y/n): ")
    if answer.lower() == 'n':
        break
