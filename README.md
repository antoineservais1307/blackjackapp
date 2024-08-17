# 🃏 Blackjack Game with Streamlit
Welcome to the Blackjack Game built with Python and Streamlit! This simple web-based game allows you to play Blackjack against a dealer with an intuitive interface, complete with card images and betting mechanics.

## 🎮 Features
* Start with $1000: Each player starts the game with a balance of $1000.
* Place Bets: Players can place bets before each round, with the option to bet any amount up to their current balance.
* Interactive Gameplay: Hit or Stand - your choice! See your cards and the dealer's up close.
* Card Images: Enjoy a more immersive experience with card images for each dealt card.
* Automatic Dealer Logic: The dealer will continue drawing cards until their hand is worth at least 17 points.
* Balance Tracking: Your balance updates after each round, reflecting wins and losses.
* Game Over Condition: If your balance drops to zero, the game is over!
## 🛠️ Installation
### Clone the repository:

```bash
Copier le code
git clone https://github.com/yourusername/blackjack-streamlit.git
```
### Navigate into the project directory:

```bash
Copier le code
cd blackjack-streamlit
```
### Install the required dependencies:

```bash
Copier le code
pip install -r requirements.txt
```
#### Make sure Streamlit and Pillow are installed.

## Run the application:

```bash
Copier le code
streamlit run app.py
```

Access the game:
Open your web browser and go to : 
- http://localhost:8501.

PS you can also go to : 

## 🃏 How to Play
### Start the game:

Click the "Start New Game" button to shuffle the deck and deal two cards to both the player and the dealer.

### Place a bet:
Use the number input to place your bet before starting a new round.

### Hit or Stand:
Choose "Hit" to draw another card or "Stand" to keep your current hand.

### Winning/Losing:

- If your hand exceeds 21, you "Bust" and lose your bet.
- If you stand, the dealer will reveal their hand and draw until they reach at least 17 points.
- The player with the higher hand value that doesn’t exceed 21 wins the round.
### Check Your Balance:
Your balance updates after each round. If your balance reaches zero, the game ends.

## 📁 Project Structure
- app.py: Main application script containing game logic and Streamlit components.
- requirements.txt: List of dependencies required to run the application.
- cards/: Directory containing the images of the playing cards.
### 📷 Card Images
Ensure the cards/ directory contains the following images:

- 2_of_hearts.png, 3_of_diamonds.png, ..., ace_of_spades.png
hidden_card.png: Image to represent the dealer's hidden card.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you have suggestions for improvements.

## 🎉 Acknowledgements
Thanks to the Streamlit community for their amazing support and tools that make creating web apps easy and fun!