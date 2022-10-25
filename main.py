from turtle import width
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.metrics import dp    
from kivy.core.window import Window

from PIL import Image as PILImage

WINDOW_SIZE = (800, 600)
Window.size = (WINDOW_SIZE[0], WINDOW_SIZE[1])

class EscapeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)    
        global WINDOW_SIZE    
        #!!!!
        # Keyboard Management
        #!!!!

        self.jump = False
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.shift = False
        self.ctrl = False

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # Value Initalization
        self.playerSpeed = 2.5
        self.movable = False
        self.animation = "Up"
        self.animationFrame = 0
        self.grounded = False

        #!!!!
        # Widget Initialization
        #!!!!
        self.bgSizes = PILImage.open("level01.png")
        self.bgPixels = self.bgSizes.convert("RGB")
        self.bg = Image(source="level01.png", width=self.bgSizes.width * 3.125, height=self.bgSizes.height * 3.75, allow_stretch=True, keep_ratio=False)
        self.bg.texture.mag_filter = "nearest"
        self.add_widget(self.bg)

        self.player = Image(source="./animations/player_0_0.png", width=dp(120), height=dp(120), allow_stretch=True)
        self.player.texture.mag_filter = "nearest"
        self.add_widget(self.player)
        self.player.pos[1] = dp(25)
        self.player.pos[0] = dp(100)

        self.playerDot = Rectangle

        # UPDATE

        Clock.schedule_interval(self.update, 1/60)
        self.right = False

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 32:
            self.jump = True
        if keycode[0] == 119:
            self.up = True
        if keycode[0] == 97:
            self.left = True
        if keycode[0] == 115:
            self.down = True
        if keycode[0] == 100:
            self.right = True
        if keycode[0] == 304:
            self.shift = True
        if keycode[0] == 305:
            self.ctrl = True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[0] == 32:
            self.jump = False
        if keycode[0] == 119:
            self.up = False
        if keycode[0] == 97:
            self.left = False
        if keycode[0] == 115:
            self.down = False
        if keycode[0] == 100:
            self.right = False
        if keycode[0] == 304:
            self.shift = False
        if keycode[0] == 305:
            self.ctrl = False

    def update(self, deltaTime, **kwargs):
        #Movement
        if self.movable:
            if self.left == True:
                self.bg.pos[0] += 100 * deltaTime * self.playerSpeed
            if self.right == True:
                self.bg.pos[0] -= 100 * deltaTime * self.playerSpeed
            if self.down == True and self.grounded == True:
                Clock.unschedule(self.moveAnimation)
                self.down = False
                self.animationFrame = 16
                Clock.schedule_interval(self.downAnimation, 1/30)
        elif self.up == True:
            self.up = False
            self.animationFrame = -1
            Clock.schedule_interval(self.upAnimation, 1/30)

        #Colision

        # if self.movable: #collision doesent need to be done when not moving
        #     if self.bgPixels.getpixel((self.player.pos[0], self.player.pos[1] - 1)) == (255, 255, 255):
        #         self.grounded = True
        #     else:
        #         self.grounded = False
        #         self.player.pos[1] -= 1
        

    def upAnimation(self, deltaTime):
        self.animationFrame += 1
        self.player.source = "./animations/player_0_" + str(self.animationFrame) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame >=15:
            self.movable = True
            Clock.unschedule(self.upAnimation)
            self.animationFrame = 11
            Clock.schedule_interval(self.moveAnimation, 1/30)

    def downAnimation(self, deltaTime):
        self.animationFrame -= 1
        self.player.source = "./animations/player_0_" + str(self.animationFrame) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame <= 0:
            self.movable = False
            Clock.unschedule(self.downAnimation)

    def moveAnimation(self, deltaTime):
        self.animationFrame += 1
        self.player.source = "./animations/player_0_" + str(self.animationFrame) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame >= 15:
            self.animationFrame = 11
            


class MainApp(App):
    pass

if __name__ == "__main__":
    MainApp().run()
