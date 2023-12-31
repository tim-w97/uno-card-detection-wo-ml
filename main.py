import config
import cv2

import speaker
from uno_classes import *
from robotPlayer import RobotPlayer
from player import HumanPlayer
from game import Game

from detector import predict_uno_cards

"""
TODO:
- Analyze the initial card
- Analyze the robot's cardstack
"""

"""
# predict initial stack card
stack_cards = []

while len(stack_cards) != 1:
    stack_cards = predict_uno_cards(config.stack_camera)

    if len(stack_cards) == 0:
        input("Detected no card on the stack. Press return to try again.")

    if len(stack_cards) > 1:
        input("Detected more than one card on the stack. Press return to try again.")
"""


# for testing
# init_card = UnoCard(color=Color.BLUE, number=9)

cards = []

while True:
    cards = predict_uno_cards(config.robot_camera)

    if len(cards) != config.card_amount:
        speaker.speak('speech/ensure seven cards.mp3')
        input("Press return to try again")
    else:
        break

speaker.speak("speech/my name is rob lets play uno together.mp3")

# init the players
robotPlayer = RobotPlayer("Rob", cards)
player = HumanPlayer("Lukas")

# run the game
game = Game(robotPlayer, player)
game.run_game()

# cleanup
cv2.destroyAllWindows()