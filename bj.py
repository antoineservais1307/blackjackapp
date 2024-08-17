import streamlit as st
import random
from PIL import Image


st.title('🎰 Blackjack 🎰')

# Initialize the game state
if 'balance' not in st.session_state:
    st.session_state.balance = 1000  # starting balance
if 'deck' not in st.session_state:
    st.session_state.deck = []
if 'player_hand' not in st.session_state:
    st.session_state.player_hand = []
if 'player_hand_split' not in st.session_state:
    st.session_state.player_hand_split = []  # Second hand after splitting
if 'dealer_hand' not in st.session_state:
    st.session_state.dealer_hand = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'bet' not in st.session_state:
    st.session_state.bet = 0
if 'split_active' not in st.session_state:
    st.session_state.split_active = False  # Track if the player has split

# Function to initialize a deck
def initialize_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

# Function to calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card, suit in hand:
        if card in ['jack', 'queen', 'king']:
            value += 10
        elif card == 'ace':
            ace_count += 1
            value += 11
        else:
            value += int(card)
    while ace_count > 0 and value > 21:
        value -= 10
        ace_count -= 1
    return value

# Function to deal cards
def deal_card(hand):
    card = st.session_state.deck.pop()
    hand.append(card)

# Function to check if the hand is a Blackjack
def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand_value(hand) == 21

# Function to display card images
def display_card_images(hand, hide_dealer_card=False):
    card_images = []
    for i, (rank, suit) in enumerate(hand):
        if i == 0 and hide_dealer_card:
            card_image_path = "cards/hidden_card.png"
        else:
            card_image_path = f"cards/{rank}_of_{suit}.png"
        card_image = Image.open(card_image_path)
        card_images.append(card_image)
    return card_images

# Betting
st.write(f"Your balance: ${st.session_state.balance}")
bet = st.number_input('Place your bet:', min_value=1, max_value=st.session_state.balance, value=10)

if st.button('Start New Game'):
    st.session_state.deck = initialize_deck()
    st.session_state.player_hand = []
    st.session_state.player_hand_split = []
    st.session_state.dealer_hand = []
    st.session_state.game_over = False
    st.session_state.split_active = False
    st.session_state.bet = bet

    deal_card(st.session_state.player_hand)
    deal_card(st.session_state.player_hand)
    deal_card(st.session_state.dealer_hand)
    deal_card(st.session_state.dealer_hand)

    # Check for immediate Blackjack for the player
    if is_blackjack(st.session_state.player_hand):
        dealer_value = calculate_hand_value(st.session_state.dealer_hand)
        if dealer_value == 21 and not is_blackjack(st.session_state.dealer_hand):
            st.write("You have a Blackjack and the dealer has 21 but not a Blackjack! You win 2.5 times your bet!")
            st.session_state.balance += 2.5 * st.session_state.bet
        else:
            st.write("Blackjack! You win 2.5 times your bet!")
            st.session_state.balance += 2.5 * st.session_state.bet
        st.session_state.game_over = True

# Game Status
if len(st.session_state.player_hand) > 0 and not st.session_state.game_over:
    # Display first hand
    st.write("Your Hand:")
    player_card_images = display_card_images(st.session_state.player_hand)
    st.image(player_card_images, width=100)

    if st.session_state.split_active:
        st.write("Your Split Hand:")
        player_split_card_images = display_card_images(st.session_state.player_hand_split)
        st.image(player_split_card_images, width=100)

    # Display dealer's hand with one card hidden
    st.write("Dealer's Hand:")
    dealer_card_images = display_card_images(st.session_state.dealer_hand, hide_dealer_card=True)
    st.image(dealer_card_images, width=100)

    player_value = calculate_hand_value(st.session_state.player_hand)
    dealer_value = calculate_hand_value(st.session_state.dealer_hand)

    st.write(f"Your Hand Value: {player_value}")

    # Handle splitting
    if len(st.session_state.player_hand) == 2 and st.session_state.player_hand[0][0] == st.session_state.player_hand[1][0]:
        if st.button('Split'):
            st.session_state.split_active = True
            st.session_state.bet *= 2
            st.session_state.player_hand_split.append(st.session_state.player_hand.pop())

            deal_card(st.session_state.player_hand)
            deal_card(st.session_state.player_hand_split)

            # Handle special case for splitting aces
            if st.session_state.player_hand[0][0] == 'ace' and st.session_state.player_hand_split[0][0] == 'ace':
                st.write("You split aces. Each hand gets one card.")
                st.session_state.game_over = True

    # Handle hitting for split or main hand
    if st.button('Hit') and not st.session_state.game_over:
        if st.session_state.split_active and len(st.session_state.player_hand_split) > 0:
            deal_card(st.session_state.player_hand_split)
            player_value_split = calculate_hand_value(st.session_state.player_hand_split)
            st.write("Your Split Hand:")
            player_split_card_images = display_card_images(st.session_state.player_hand_split)
            st.image(player_split_card_images, width=100)
            st.write(f"Your Split Hand Value: {player_value_split}")
            if player_value_split > 21:
                st.write("Bust on your split hand! You lose.")
                st.session_state.balance -= st.session_state.bet // 2
                st.session_state.split_active = False  # Stop playing this hand
        else:
            deal_card(st.session_state.player_hand)
            player_value = calculate_hand_value(st.session_state.player_hand)
            st.write("Your Hand:")
            player_card_images = display_card_images(st.session_state.player_hand)
            st.image(player_card_images, width=100)
            st.write(f"Your Hand Value: {player_value}")
            if player_value > 21:
                st.write("Bust! You lose.")
                st.session_state.balance -= st.session_state.bet
                st.session_state.game_over = True

    # Handle standing for split or main hand
    if st.button('Stand') and not st.session_state.game_over:
        if st.session_state.split_active and len(st.session_state.player_hand_split) > 0:
            st.session_state.split_active = False  # Finish playing the split hand
        else:
            while dealer_value < 17:
                deal_card(st.session_state.dealer_hand)
                dealer_value = calculate_hand_value(st.session_state.dealer_hand)
            st.write("Dealer's Hand:")
            dealer_card_images = display_card_images(st.session_state.dealer_hand)
            st.image(dealer_card_images, width=100)
            st.write(f"Dealer's Hand Value: {dealer_value}")

            if st.session_state.split_active:
                player_value_split = calculate_hand_value(st.session_state.player_hand_split)
                if dealer_value > 21 or player_value_split > dealer_value:
                    st.write("You win on your split hand!")
                    st.session_state.balance += st.session_state.bet
                elif player_value_split == dealer_value:
                    st.write("Push on your split hand! Bet returned.")
                else:
                    st.write("You lose on your split hand!")
                    st.session_state.balance -= st.session_state.bet // 2

            if dealer_value == 21 and not is_blackjack(st.session_state.dealer_hand) and is_blackjack(st.session_state.player_hand):
                st.write("You have a Blackjack and the dealer has 21 but not a Blackjack! You win 2.5 times your bet!")
                st.session_state.balance += 1.5 * st.session_state.bet
            elif dealer_value > 21 or player_value > dealer_value:
                if is_blackjack(st.session_state.player_hand):
                    st.write("Blackjack! You win 2.5 times your bet!")
                    st.session_state.balance += 1.5 * st.session_state.bet
                else:
                    st.write("You win!")
                    st.session_state.balance += st.session_state.bet
            elif player_value == dealer_value:
                st.write("Push on your main hand! Bet returned.")
            else:
                st.write("You lose!")
                st.session_state.balance -= st.session_state.bet

            st.session_state.game_over = True

# Check balance
if st.session_state.balance <= 0:
    st.write("Game Over! You are out of money.")
