import random
import time
import curses

# Constants
SUITS = ['♠', '♡', '♢', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_WIDTH = 9
CARD_HEIGHT = 7

def create_deck():
    # Create a deck of cards by combining all ranks and suits, then shuffle it
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    # Calculate the value of a hand in Blackjack
    value = 0
    has_ace = False

    for rank, suit in hand:
        if rank.isdigit():
            value += int(rank)
        elif rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            value += 11
            has_ace = True

    # Adjust the value if the hand has an Ace and the total value is over 21
    if has_ace and value > 21:
        value -= 10
    return value

def display_cards(stdscr, cards):
    # Display the cards on the screen using ASCII art
    stdscr.clear()

    for i, card in enumerate(cards):
        rank, suit = card
        x = i * CARD_WIDTH
        y = 0

        stdscr.addstr(y, x, '┌───────┐')
        stdscr.addstr(y + 1, x, f'│ {rank:<2}    │')
        stdscr.addstr(y + 2, x, '│       │')
        stdscr.addstr(y + 3, x, f'│   {suit}   │')
        stdscr.addstr(y + 4, x, '│       │')
        stdscr.addstr(y + 5, x, f'│    {rank:>2} │')
        stdscr.addstr(y + 6, x, '└───────┘')

    stdscr.refresh()

def play_again(stdscr):
    # Ask the player if they want to play again
    stdscr.refresh()

    while True:
        stdscr.addstr(9, 0, 'Do you want to play again? (y/n): ')
        stdscr.refresh()
        answer = stdscr.getkey().lower()

        if answer in ['y', 'n']:
            return answer == 'y'
        else:
            stdscr.addstr(10, 0, 'Please enter either "y" or "n".')
            stdscr.refresh()

def delayed_print(stdscr, text, delay=0.03):
    # Print text on the screen with a delay between characters
    for char in text:
        stdscr.addstr(char)
        stdscr.refresh()
        time.sleep(delay)

def welcome_message(stdscr):
    # Display the welcome message and ask the player if they are ready to play
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)
    delayed_print(stdscr, """Welcome to Austin's illegal, underground Linux Gambling Ring!
Tonight's game... Blackjack!     

The rules are simple!
  - You are individually dealt cards, and you can freely choose when to stop.
  - The objective is to remain below 21 while aiming to be the closest to it.
        """, 0.025)
    stdscr.addstr('\nAre you ready?')
    choice = stdscr.getkey().lower()
    return choice

def deal_initial_cards(deck):
    # Deal two cards each to the player and the dealer from the deck
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    return player_hand, dealer_hand

def handle_player_choice(stdscr, deck, player_hand):
    stdscr.addstr(f'\nYou have a score of {calculate_hand_value(player_hand)}.')
    stdscr.addstr('\nDo you want to hit or stand? (h/s): ')
    stdscr.refresh()
    choice = stdscr.getkey().lower()

    while choice == 'h':
        player_hand.append(deck.pop())
        delayed_print(stdscr, '\nYou decide to hit...')
        display_cards(stdscr, player_hand)

        if calculate_hand_value(player_hand) > 21:
            delayed_print(stdscr, f'\nBust! You lose! ({calculate_hand_value(player_hand)})')

            if not play_again(stdscr):
                return None
            else:
                return 'continue'

        stdscr.addstr('\nDo you want to hit or stand? (h/s): ')
        stdscr.refresh()
        choice = stdscr.getkey().lower()

    if choice == 's':
        delayed_print(stdscr, '\nYou decide to stand.')
        return 'stand'
    else:
        delayed_print(stdscr, '\nPlease enter either "h" or "s".')

    return 'continue'

def handle_dealer_play(stdscr, deck, dealer_hand):
    # Handle the dealer's turn to play
    stdscr.clear()
    stdscr.refresh()

    delayed_print(stdscr, 'Now, the dealer\'s hand!')
    time.sleep(1)
    display_cards(stdscr, dealer_hand)
    time.sleep(1)

    while calculate_hand_value(dealer_hand) < 17:
        delayed_print(stdscr, '\nDealer decides to hit...')
        dealer_hand.append(deck.pop())
        display_cards(stdscr, dealer_hand)
        time.sleep(1)

    dealer_value = calculate_hand_value(dealer_hand)
    return dealer_value

def determine_winner(stdscr, dealer_value, player_value):
    # Determine the winner based on the values of the dealer's and player's hands
    if dealer_value > 21:
        delayed_print(stdscr, f'\nDealer busts! You win! ({dealer_value})')
    elif dealer_value > player_value:
        delayed_print(stdscr, "\nDealer decides to stand...")
        delayed_print(stdscr, f'\nDealer wins! ({dealer_value} > {player_value})')
    elif dealer_value < player_value:
        delayed_print(stdscr, "\nDealer decides to stand...")
        delayed_print(stdscr, f'\nYou win! ({dealer_value} < {player_value})')
    else:
        delayed_print(stdscr, '\nIt\'s a tie!')

def main(stdscr):
    while True:
        deck = create_deck()
        player_hand, dealer_hand = deal_initial_cards(deck)

        stdscr.addstr('Your Hand:')
        display_cards(stdscr, player_hand)

        if calculate_hand_value(player_hand) == 21:
            delayed_print(stdscr, '\nBlackjack! You win!')

            if not play_again(stdscr):
                return
            else:
                continue

        choice = handle_player_choice(stdscr, deck, player_hand)
        if choice is None:
            return
        elif choice == 'stand':
            dealer_value = handle_dealer_play(stdscr, deck, dealer_hand)
            player_value = calculate_hand_value(player_hand)

            if player_value <= 21:
                time.sleep(0.5)
                stdscr.clear()
                stdscr.refresh()

                determine_winner(stdscr, dealer_value, player_value)

        if not play_again(stdscr):
            return

if __name__ == '__main__':
    curses.wrapper(welcome_message)
    curses.wrapper(main)
