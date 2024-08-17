import streamlit as st
import random
from PIL import Image

st.set_page_config(page_title="🎰 Blackjack 🎰", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2em;
        color: #ffcc00;
    }
    .button {
        display: block;
        margin: 0 auto;
    }
    .card {
        display: inline-block;
        margin: 5px;
    }
    .container {
        background: url('https://example.com/background.jpg') no-repeat center center fixed;
        background-size: cover;
        padding: 20px;
        border-radius: 15px;
    }
    .error {
        color: red;
        text-align: center;
        font-size: 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎰 Blackjack 🎰</div>', unsafe_allow_html=True)

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
if 'doubled_down' not in st.session_state:
    st.session_state.doubled_down = False  # Track if the player has doubled down
if 'current_hand' not in st.session_state:
    st.session_state.current_hand = 'main'  # Track which hand the player is currently playing
if 'hands_played' not in st.session_state:
    st.session_state.hands_played = {'main': False, 'split': False}  # Track if each hand has been played
if 'error_message' not in st.session_state:
    st.session_state.error_message = None  # Track any error messages

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

# Container for the game
with st.container():
    st.write(f"Your balance: ${st.session_state.balance}")
    
    if st.session_state.balance <= 0:
        st.markdown('<div class="error">Game Over! You are out of money.</div>', unsafe_allow_html=True)
        st.stop()  # Stop the execution of the script if balance is zero
    
    # Ensure all numerical values are integers
    bet = st.number_input('Place your bet:', min_value=1, max_value=int(st.session_state.balance), value=10, step=1)
    
    if st.button('Start New Game', key='start', use_container_width=True):
        if st.session_state.balance < bet:
            st.markdown('<div class="error">Insufficient balance to place this bet!</div>', unsafe_allow_html=True)
        else:
            st.session_state.deck = initialize_deck()
            st.session_state.player_hand = []
            st.session_state.player_hand_split = []
            st.session_state.dealer_hand = []
            st.session_state.game_over = False
            st.session_state.split_active = False
            st.session_state.doubled_down = False
            st.session_state.bet = bet
            st.session_state.current_hand = 'main'
            st.session_state.hands_played = {'main': False, 'split': False}
            st.session_state.error_message = None

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

    if len(st.session_state.player_hand) > 0 and not st.session_state.game_over:
        # Display first hand
        st.write("Your Hand:")
        player_card_images = display_card_images(st.session_state.player_hand)
        st.image(player_card_images, width=150, use_column_width=False)

        if st.session_state.split_active:
            st.write("Your Split Hand:")
            player_split_card_images = display_card_images(st.session_state.player_hand_split)
            st.image(player_split_card_images, width=150, use_column_width=False)

        # Display dealer's hand with one card hidden
        st.write("Dealer's Hand:")
        dealer_card_images = display_card_images(st.session_state.dealer_hand, hide_dealer_card=True)
        st.image(dealer_card_images, width=150, use_column_width=False)

        player_value = calculate_hand_value(st.session_state.player_hand)
        dealer_value = calculate_hand_value(st.session_state.dealer_hand)
        split_value = calculate_hand_value(st.session_state.player_hand_split) if st.session_state.split_active else None

        st.write(f"Your Hand Value: {player_value}")

        # Handle splitting
        def can_split():
            return st.session_state.balance >= st.session_state.bet * 2

        # Handle doubling down
        def can_double_down():
            return st.session_state.balance >= st.session_state.bet * 2

        if len(st.session_state.player_hand) == 2 and st.session_state.player_hand[0][0] == st.session_state.player_hand[1][0]:
            if st.button('Split', key='split', use_container_width=True):
                if can_split():
                    st.session_state.split_active = True
                    st.session_state.bet *= 2
                    st.session_state.player_hand_split.append(st.session_state.player_hand.pop())

                    deal_card(st.session_state.player_hand)
                    deal_card(st.session_state.player_hand_split)

                    # Handle special case for splitting aces
                    if st.session_state.player_hand[0][0] == 'ace' and st.session_state.player_hand_split[0][0] == 'ace':
                        st.write("You split aces. Each hand gets one card.")
                        st.session_state.game_over = True
                else:
                    st.markdown('<div class="error">Insufficient balance to split!</div>', unsafe_allow_html=True)

        if len(st.session_state.player_hand) == 2 and not st.session_state.doubled_down:
            if st.button('Double Down', key='double_down', use_container_width=True):
                if can_double_down():
                    st.session_state.doubled_down = True
                    st.session_state.balance -= st.session_state.bet
                    st.session_state.bet *= 2
                    deal_card(st.session_state.player_hand)
                    player_value = calculate_hand_value(st.session_state.player_hand)
                    st.write("Your Hand:")
                    player_card_images = display_card_images(st.session_state.player_hand)
                    st.image(player_card_images, width=150, use_column_width=False)
                    st.write(f"Your Hand Value: {player_value}")
                    if player_value > 21:
                        st.write("Bust! You lose.")
                        st.session_state.balance -= st.session_state.bet
                        st.session_state.game_over = True
                else:
                    st.markdown('<div class="error">Insufficient balance to double down!</div>', unsafe_allow_html=True)

        # Actions for main hand
        if st.session_state.current_hand == 'main':
            if st.button('Hit', key='hit', use_container_width=True) and not st.session_state.game_over:
                if st.session_state.doubled_down:
                    st.session_state.error_message = "You have doubled down and cannot hit."
                else:
                    deal_card(st.session_state.player_hand)
                    player_value = calculate_hand_value(st.session_state.player_hand)
                    st.write("Your Hand:")
                    player_card_images = display_card_images(st.session_state.player_hand)
                    st.image(player_card_images, width=150, use_column_width=False)
                    st.write(f"Your Hand Value: {player_value}")
                    if player_value > 21:
                        st.write("Bust! You lose.")
                        st.session_state.balance -= st.session_state.bet
                        st.session_state.game_over = True

            if st.button('Stand', key='stand', use_container_width=True) and not st.session_state.game_over:
                st.session_state.hands_played['main'] = True
                if st.session_state.split_active:
                    st.session_state.current_hand = 'split'
                else:
                    st.session_state.game_over = True

        # Actions for split hand
        if st.session_state.current_hand == 'split' and st.session_state.split_active:
            if st.button('Hit on Split Hand', key='hit_split', use_container_width=True) and not st.session_state.game_over:
                if st.session_state.doubled_down:
                    st.session_state.error_message = "You have doubled down and cannot hit."
                else:
                    deal_card(st.session_state.player_hand_split)
                    split_value = calculate_hand_value(st.session_state.player_hand_split)
                    st.write("Your Split Hand:")
                    player_split_card_images = display_card_images(st.session_state.player_hand_split)
                    st.image(player_split_card_images, width=150, use_column_width=False)
                    st.write(f"Your Split Hand Value: {split_value}")
                    if split_value > 21:
                        st.write("Bust on your split hand! You lose.")
                        st.session_state.balance -= st.session_state.bet // 2
                        st.session_state.hands_played['split'] = True
                        st.session_state.current_hand = 'main' if not st.session_state.hands_played['main'] else None
                        if not st.session_state.current_hand:
                            st.session_state.game_over = True

            if st.button('Stand on Split Hand', key='stand_split', use_container_width=True) and not st.session_state.game_over:
                st.session_state.hands_played['split'] = True
                st.session_state.current_hand = 'main' if not st.session_state.hands_played['main'] else None
                if not st.session_state.current_hand:
                    st.session_state.game_over = True

        # Show error message if exists
        if st.session_state.error_message:
            st.markdown(f'<div class="error">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        # Evaluate game results
        if st.session_state.game_over:
            if st.session_state.hands_played['main']:
                # Dealer's turn
                while dealer_value < 17:
                    deal_card(st.session_state.dealer_hand)
                    dealer_value = calculate_hand_value(st.session_state.dealer_hand)

                st.write("Dealer's Final Hand:")
                dealer_card_images = display_card_images(st.session_state.dealer_hand)
                st.image(dealer_card_images, width=150, use_column_width=False)
                st.write(f"Dealer's Hand Value: {dealer_value}")

                # Main hand results
                if calculate_hand_value(st.session_state.player_hand) > 21:
                    st.write("Bust on main hand! You lose.")
                    st.session_state.balance -= st.session_state.bet
                elif dealer_value > 21:
                    st.write("Dealer busts! You win on main hand.")
                    st.session_state.balance += st.session_state.bet
                elif dealer_value < calculate_hand_value(st.session_state.player_hand):
                    st.write("You win on main hand!")
                    st.session_state.balance += st.session_state.bet
                elif dealer_value > calculate_hand_value(st.session_state.player_hand):
                    st.write("Dealer wins on main hand!")
                    st.session_state.balance -= st.session_state.bet
                else:
                    st.write("Push on main hand! It's a tie.")

                # Split hand results
                if st.session_state.hands_played['split']:
                    split_value = calculate_hand_value(st.session_state.player_hand_split)
                    if split_value > 21:
                        st.write("Bust on split hand! You lose.")
                        st.session_state.balance -= st.session_state.bet // 2
                    elif dealer_value > 21:
                        st.write("Dealer busts! You win on split hand.")
                        st.session_state.balance += st.session_state.bet // 2
                    elif dealer_value < split_value:
                        st.write("You win on split hand!")
                        st.session_state.balance += st.session_state.bet // 2
                    elif dealer_value > split_value:
                        st.write("Dealer wins on split hand!")
                        st.session_state.balance -= st.session_state.bet // 2
                    else:
                        st.write("Push on split hand! It's a tie.")
