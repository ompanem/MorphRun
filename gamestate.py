from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    WIN = "win"
    DEAD = "dead"
    FINISHED = "finished"