import streamlit as st
import random
from PIL import Image

# Initialize the game state
if 'balance' not in st.session_state:
    st.session_state.balance = 1000  # starting balance
if 'deck' not in st.session_state:
    st.session_state.deck = []
if 'player_hand' not in st.session_state:
    st.session_state.player_hand = []
if 'dealer_hand' not in st.session_state:
    st.session_state.dealer_hand = []

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
    st.session_state.dealer_hand = []

    deal_card(st.session_state.player_hand)
    deal_card(st.session_state.player_hand)
    deal_card(st.session_state.dealer_hand)
    deal_card(st.session_state.dealer_hand)

# Game Status
if len(st.session_state.player_hand) > 0:
    st.write("Your Hand:")
    player_card_images = display_card_images(st.session_state.player_hand)
    st.image(player_card_images, width=100)

    st.write("Dealer's Hand:")
    dealer_card_images = display_card_images(st.session_state.dealer_hand, hide_dealer_card=True)
    st.image(dealer_card_images, width=100)

    player_value = calculate_hand_value(st.session_state.player_hand)
    dealer_value = calculate_hand_value(st.session_state.dealer_hand)

    st.write(f"Your Hand Value: {player_value}")

    if st.button('Hit'):
        deal_card(st.session_state.player_hand)
        player_value = calculate_hand_value(st.session_state.player_hand)
        st.write("Your Hand:")
        player_card_images = display_card_images(st.session_state.player_hand)
        st.image(player_card_images, width=100)
        st.write(f"Your Hand Value: {player_value}")
        if player_value > 21:
            st.write("Bust! You lose.")
            st.session_state.balance -= bet
    elif st.button('Stand'):
        while dealer_value < 17:
            deal_card(st.session_state.dealer_hand)
            dealer_value = calculate_hand_value(st.session_state.dealer_hand)
        st.write("Dealer's Hand:")
        dealer_card_images = display_card_images(st.session_state.dealer_hand)
        st.image(dealer_card_images, width=100)
        st.write(f"Dealer's Hand Value: {dealer_value}")
        if dealer_value > 21 or player_value > dealer_value:
            st.write("You win!")
            st.session_state.balance += bet
        else:
            st.write("You lose!")
            st.session_state.balance -= bet

# Check balance
if st.session_state.balance <= 0:
    st.write("Game Over! You are out of money.")
