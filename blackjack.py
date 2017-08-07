from random import shuffle
from time import sleep

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = 'cards\{}_{}.{}'.format(str(card), suit, extension)
            image = PhotoImage(file=name)
            card_images.append((card, image))

        # next the face cards
        for card in face_cards:
            name = 'cards\{}_{}.{}'.format(str(card), suit, extension)
            image = PhotoImage(file=name)
            card_images.append((10, image))


def _deal_card(frame):
    # pop the next card off the top of the deck
    try:
        next_card = deck.pop(0)
    except IndexError:
        result_text.set("Deck is empty!")
        return
    # add the image to a Label() and display the label
    Label(frame, image=next_card[1], relief='raised').pack(side='left')     # perfect for pack() **
    return next_card


def deal_dealer():
    dealer_score = score_hand(dealer_hand)

    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        sleep(0.25)
        dealer_card_frame.update()
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player Wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins!")
    else:
        result_text.set("Draw!")


def score_hand(hand):
    # Calculate the total score of all cards in the list.
    # Only one ace can have the value 11. and this will be reduce to 1 if the hand would bust.
    # This will make it useless to use a global player and dealer score variable

    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_player():
    player_score = score_hand(player_hand)

    player_hand.append(_deal_card(player_card_frame))
    if player_score > 21:
        result_text.set("Dealer Wins!")
    player_score_label.set(player_score)
    print(locals(), end='  ')
    print("{'player_score': " + str(player_score) + '}')


def inital_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # embedded frame to hold the card images
    result_text.set("")
    dealer_card_frame.destroy()
    dealer_card_frame = Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    player_card_frame.destroy()
    player_card_frame = Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    dealer_hand = []
    player_hand = []

    player_score_label.set(score_hand(player_hand))
    dealer_score_label.set(score_hand(dealer_hand))

    inital_deal()


def shuffle_deck():
    shuffle(deck)


def play():
    inital_deal()
    root.mainloop()


root = Tk()
root.title("Black Jack")
root.geometry("800x275")
root.configure(background='green')

result_text = StringVar()
result = Label(root, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = Frame(root, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = IntVar()
Label(card_frame, text='Dealer', background='green', fg='white').grid(row=0, column=0)
Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)

# embedded frame to hold the card images
dealer_card_frame = Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = IntVar()
Label(card_frame, text='Player', background='green', fg='white').grid(row=2, column=0)
Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

# embedded frame to hold the card images for the player
player_card_frame = Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = Frame(root)
button_frame.grid(row=4, column=0, columnspan=3, sticky='w')

dealer_button = Button(button_frame, text='Dealer', command=deal_dealer).grid(row=0, column=0)
player_button = Button(button_frame, text='Player', command=deal_player).grid(row=0, column=1)
reset_button = Button(button_frame, text='New Game', command=new_game).grid(row=0, column=2)
shuffle_button = Button(button_frame, text='Shuffle Deck', command=shuffle_deck).grid(row=0, column=3)

# load cards
cards = []
load_images(cards)
print(cards)

# create a new deck of cards and shuffle them
deck = list(cards) + list(cards) + list(cards) + list(cards)  # NOTE !!! list() will create a new list
#  while deck=cards can mutate the original cards list
shuffle_deck()

# create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == '__main__':
    play()

"""
    **NOTE** Using pack and grid together is a very bad idea which will cause errors by the python3 compiler.
    -> Although using a different geometry manager in a new frame as the only manager for the frame is okay!
    Pack will in this example just stack the cards created on the side of the others which makes it perfect
    in this scenario.
"""
