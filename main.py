from turtle import width
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
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

        #!!!!
        # Widget Initialization
        #!!!!

        bgSizes = (PILImage.open("level01.png").width, PILImage.open("level01.png").height)
        self.bg = Image(source="level01.png", height=str(bgSizes[1] * 3.75), width=bgSizes[0] * 3.125, allow_stretch=True, keep_ratio=False)
        self.bg.texture.mag_filter = "nearest"
        self.add_widget(self.bg)

        self.player = Image(source="./animations/player_0_0.png", width=dp(120), height=dp(120), allow_stretch=True)
        self.player.texture.mag_filter = "nearest"
        self.add_widget(self.player)
        self.player.pos[1] = dp(10)

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
            Clock
            if self.left:
                self.player.pos[0] += -100 * deltaTime * self.playerSpeed
            if self.right:
                self.player.pos[0] += 100 * deltaTime * self.playerSpeed
            if self.down:
                self.animationFrame = 15
                Clock.schedule_interval(self.downAnimation, 1/60)
        elif self.up:
            self.animationFrame = 0
            Clock.schedule_interval(self.upAnimation, 1/60) #gets trigerred multiple times!!!

    def upAnimation(self, deltaTime):
        self.animationFrame += 0.1
        print("./animations/sprite_" + str(round(self.animationFrame)) + ".png")
        self.player.source = "./animations/player_0_" + str(round(self.animationFrame)) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame >=15:
            self.movable = True
            Clock.unschedule(self.upAnimation)

    def downAnimation(self, deltaTime):
        self.animationFrame -= 0.1
        self.player.source = "./animations/player_0_" + str(round(self.animationFrame)) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame <= 0:
            self.movable = False
            Clock.unschedule(self.downAnimation)

    def moveAnimation(self, deltaTime):
        self.animationFrame -= 0.1
        self.player.source = "./animations/player_0_" + str(round(self.animationFrame)) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame <= 0:
            self.movable = False
            Clock.unschedule(self.downAnimation)
            


class MainApp(App):
    pass

if __name__ == "__main__":
    MainApp().run()
