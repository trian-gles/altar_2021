from pyo import *


ALL_CARDS = []


class AudioCard:
    def __init__(self):
        ALL_CARDS.append(self)

audio_cards = [AudioCard() for _ in range(52)]