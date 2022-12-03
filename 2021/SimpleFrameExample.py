import libraries.simpleframe as sf
from libraries.simpleframe import SimpleFrame
import math

# Overide method draw of class SimpleFrame
class Bot(SimpleFrame):
    def draw(self):
        for i in range(100):
            self.reset_background()
            self.display_text(str(i), 200, 200, color = sf.BLACK)
            self.draw_tile((i % 20,i*i % 20), sf.BLUE)
            self.refresh()
            self.check_closed()

a = Bot(tile_size = 10, frame_rate=0.1)
a.set_title("Test draw")
a.set_font('Comic Sans MS', 30)
a.draw()