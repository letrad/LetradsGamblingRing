import random
import time
import curses

# This creates a deck of cards using a Tuple Array.
def createDeck():
    deck = []
    suits = ['♠', '♡', '♢', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    for suit in suits:
        for rank in ranks:
            card = (rank, suit)
            deck.append(card)

    random.shuffle(deck)
    return deck

# Function to calculate the value of a hand
def calcHandValue(hand):
    value = 0
    has_ace = False

    for card in hand:
        rank = card[0]
        if rank.isdigit():
            value += int(rank)
        elif rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            value += 11
            has_ace = True

    # Adjust the value if there is an Ace and the hand value exceeds 21. As Aces can be recognized as 1 or 11.
    if has_ace and value > 21:
        value -= 10
    return value

# Function to display the cards
def displayCards(stdscr, cards):
    stdscr.clear()
    stdscr.refresh()

    for i, card in enumerate(cards):
        rank, suit = card

        stdscr.addstr(0, i * 9, '┌───────┐')
        stdscr.addstr(1, i * 9, f'│ {rank:<2}    │')
        stdscr.addstr(2, i * 9, '│       │')
        stdscr.addstr(3, i * 9, f'│   {suit}   │')
        stdscr.addstr(4, i * 9, '│       │')
        stdscr.addstr(5, i * 9, f'│    {rank:>2} │')
        stdscr.addstr(6, i * 9, '└───────┘')

    stdscr.refresh()

# Function to check if the player wants to play again
def playAgain(stdscr):
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


# Function to print text with a delay to simulate typing effect
def delayedPrint(stdscr, text, delay=0.03):
    for char in text:
        stdscr.addstr(char)
        stdscr.refresh()
        time.sleep(delay)

def firstStart(stdscr):
    while True:
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(0)
        delayedPrint(stdscr, """Welcome to Austin's illegal, underground Linux Gambling Ring!
Tonight\'s game... Blackjack!     
   
The Rules are simple!
  - You are individually dealt cards, and you can freely choice when to stop.
  - The objective is to remain below 21, while also aiming to be the closest to it
        """, 0.025)
        stdscr.addstr('\nAre ye ready?')
        choice = stdscr.getkey().lower()
        if choice is not None:
            break
    return

# Main game loop + logic
def main(stdscr):

    deck = createDeck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    stdscr.addstr('Your Hand:')
    displayCards(stdscr, player_hand)

    # Check if player has blackjack
    if calcHandValue(player_hand) == 21:
        delayedPrint(stdscr, '\nBlackjack! You win!')
        if not playAgain(stdscr):
            return
        else:
            main(stdscr)

    # Player's turn
    while True:
        stdscr.addstr(f'\nYou have a score of {calcHandValue(player_hand)}.')
        stdscr.addstr('\nDo you want to hit or stand? (h/s): ')
        stdscr.refresh()
        choice = stdscr.getkey().lower()

        if choice == 'h':
            player_hand.append(deck.pop())
            delayedPrint(stdscr, '\nYou decide to hit...')
            displayCards(stdscr, player_hand)

            if calcHandValue(player_hand) > 21:
                delayedPrint(stdscr, f'\nBust! You lose! ({calcHandValue(player_hand)})')

                if not playAgain(stdscr):
                    return
                else:
                    main(stdscr)
        elif choice == 's':
            delayedPrint(stdscr, '\nYou decide to stand.')
            break
        else:
            delayedPrint(stdscr, '\nPlease enter either "h" or "s".')

    # Dealer's turn
    if calcHandValue(player_hand) <= 21:
        time.sleep(0.5)
        stdscr.clear()
        stdscr.refresh()

        delayedPrint(stdscr, 'Now, the dealer\'s hand!')
        time.sleep(1)
        displayCards(stdscr, dealer_hand)
        time.sleep(1)

        while calcHandValue(dealer_hand) < 17:
            delayedPrint(stdscr, '\nDealer decides to hit...')
            dealer_hand.append(deck.pop())
            displayCards(stdscr, dealer_hand)
            time.sleep(1)

        if calcHandValue(dealer_hand) > 21:
            delayedPrint(stdscr, f'\nDealer busts! You win! ({calcHandValue(dealer_hand)})')
        elif calcHandValue(dealer_hand) > calcHandValue(player_hand):
            delayedPrint(stdscr, "\nDealer decides to stand...")
            delayedPrint(stdscr, f'\nDealer wins! ({calcHandValue(dealer_hand)} > {calcHandValue(player_hand)})')
        elif calcHandValue(dealer_hand) < calcHandValue(player_hand):
            delayedPrint(stdscr, "\nDealer decides to stand...")
            delayedPrint(stdscr, f'\nYou win! ({calcHandValue(dealer_hand)} < {calcHandValue(player_hand)})')
        else:
            delayedPrint(stdscr, '\nIt\'s a tie!')

    if not playAgain(stdscr):
        return
    else:
        main(stdscr)


if __name__ == '__main__':
    curses.wrapper(firstStart)
    curses.wrapper(main)
