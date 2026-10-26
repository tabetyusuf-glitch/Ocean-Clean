import math
import random
import arcade
screenwidth = 1000
screenheight=700
TITLE = "Ocean Cleanup"
WATER = (0, 123, 146)
class game(arcade.Window):
    def __init__(self):
        super().__init__(screenwidth, screenheight, TITLE)
        self.background_color = WATER
        def on_draw(self):
            self.clear()

game = game()
arcade.run()
