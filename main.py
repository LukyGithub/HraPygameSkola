from kivy.uix.widget import Widget
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.metrics import dp    
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from functools import partial
from PIL import Image as PILImage
import math as m

WINDOW_SIZE = (800, 600)
# Window.size = (WINDOW_SIZE[0], WINDOW_SIZE[1])

def clamp(val: int | float, miminum: int | float, maximum: int | float) -> float:
    return min(maximum, max(miminum, val))

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

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

        #!!!!
        # Widget Initialization
        #!!!!
        self.bgColor = Image(source="background.png", width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bgColor)

        self.player = Image(source="./animations/player_0_0.png", width=dp(120), height=dp(120), allow_stretch=True)
        self.player.texture.mag_filter = "nearest"
        self.add_widget(self.player)
        self.player.pos[1] = 215
        self.player.pos[0] = dp(100)

        self.enemy = []
        self.warning = []
        self.warningCircle = []
        self.enemyFrame = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.enemyX0 = [787, 1725, 1725, 2812, 2812, 2812, 2812, 2812, 2625, 2625, 2625, 5550, 5550, 6120, 6300, 6487, 7330, 7811, 6825, 6825]
        self.enemyX1 = [1362, 2250, 2250, 5000, 5000, 5000, 5000, 5000, 4300, 4300, 4300, 5850, 6000, 6121, 6301, 6488, 7355, 7881, 8250, 8250]
        self.prevEnemyPos = [787, 1725, 1725, 2812, 2812, 2812, 2812, 2812, 2625, 2625, 2625, 5550, 5550, 6120, 6300, 6487, 7330, 7811, 6825, 6825]
        self.enemyY = [57, 57, 57, 11, 11, 11, 11, 11, 255, 255, 255, 133, 375, 210, 210, 210, 191, 191, 11, 11]
        for i in range(0, 20):
            self.warningCircle.append(Image(source="warningCircle.png", width=200, height=200, allow_stretch=True, keep_ratio=False))
            self.warningCircle[i].texture.mag_filter = "nearest"
            self.warningCircle[i].opacity = 0.5
            self.add_widget(self.warningCircle[i])

            self.warning.append(None)
            self.enemy.append(Image(source="./animations/sprite_1_0.png", width=dp(120), height=dp(120), allow_stretch=True))
            self.enemy[i].texture.mag_filter = "nearest"
            self.enemy[i].pos[1] = self.enemyY[i]
            self.add_widget(self.enemy[i])

        self.bgSizes = PILImage.open("level01.png")
        self.bgCollisions = PILImage.open("level01Collisions.png")
        self.bgPixels = self.bgCollisions.convert("RGB")
        self.bg = Image(source="level01.png", width=self.bgSizes.width * 3.75, height=self.bgSizes.height * 3.75, allow_stretch=True, keep_ratio=False)
        self.bg.texture.mag_filter = "nearest"
        self.bg.pos[0] = -350
        self.add_widget(self.bg)

        # Value Initalization
        self.playerSpeed = 2.5
        self.movable = False
        self.animation = "Up"
        self.animationFrame = 0
        self.grounded = False
        self.velocity = 0
        self.jumpHeight = 750
        self.gravity = 981 * 2
        self.hitLength = 350
        self.checkScheduled = []
        self.playerWarned = []
        self.loseLength = 100
        for i in self.enemy:
            self.checkScheduled.append(False)
            self.playerWarned.append(False)

        # UPDATE
        
        self.gameSong = SoundLoader.load('gameMusicYay.mp3')
        self.gameSong.volume = 0.4
        self.riseSfx = SoundLoader.load('rockRise.mp3')
        self.settleSfx = SoundLoader.load('rockSettle.mp3')
        self.hoverSfx = SoundLoader.load('rockHover.mp3')
        self.warning1 = SoundLoader.load("warning1.mp3")
        self.warning2 = SoundLoader.load("warning2.mp3")
        self.warning3 = SoundLoader.load("warning3.mp3")
        Clock.usleep(1000000)
        self.gameSong.play()
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.playSong, self.gameSong.length)

    def _keyboard_closed(self):
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
        playerPos = (self.bg.pos[0]) * -1 + self.player.pos[0]

        #Colision (is calculated first but executed last)
        if self.movable: #collision doesen't need to be done when not moving
            if self.bgPixels.getpixel((     clamp(round((playerPos +41) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            elif self.bgPixels.getpixel((     clamp(round((playerPos +73) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            elif self.bgPixels.getpixel((     clamp(round((playerPos +57) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            elif self.bgPixels.getpixel((     clamp(round((playerPos +41) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            elif self.bgPixels.getpixel((     clamp(round((playerPos +73) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            elif self.bgPixels.getpixel((     clamp(round((playerPos +57) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
                self.velocity = 0
            else:
                self.grounded = False
                self.velocity -= self.gravity * deltaTime

        #Movement && part of colisions
        if self.movable:
            if self.left == True:
                if self.bgPixels.getpixel((     clamp(round((playerPos +36) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 1)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                    if self.bgPixels.getpixel((     clamp(round((playerPos +36) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 102)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0) and self.bgPixels.getpixel((     clamp(round((playerPos +36) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 51)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                        self.bg.pos[0] += 100 * deltaTime * self.playerSpeed
                elif self.bgPixels.getpixel((     clamp(round((playerPos +36) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - ((self.player.pos[1] + self.velocity * deltaTime + 1)/3.75 + 2)), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                    self.bg.pos[0] += 100 * deltaTime * self.playerSpeed
                    self.player.pos[1] += 6
            if self.right == True:
                # Checks for all three collision points wheather theres a wall/collision object in the way
                if  self.bgPixels.getpixel((     clamp(round((playerPos +76) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 1)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                    if self.bgPixels.getpixel((     clamp(round((playerPos +76) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 102)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0) and self.bgPixels.getpixel((     clamp(round((playerPos +76) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 51)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                        self.bg.pos[0] -= 100 * deltaTime * self.playerSpeed
                # Makes sure its not just stairs
                elif self.bgPixels.getpixel((     clamp(round((playerPos +76) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - ((self.player.pos[1] + self.velocity * deltaTime + 1)/3.75 +2)), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
                    self.bg.pos[0] -= 100 * deltaTime * self.playerSpeed
                    self.player.pos[1] += 6
            if self.bgPixels.getpixel((     clamp(round((playerPos +41) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
            elif self.bgPixels.getpixel((     clamp(round((playerPos +73) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
            elif self.bgPixels.getpixel((     clamp(round((playerPos +57) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
            elif self.bgPixels.getpixel((     clamp(round((playerPos +41) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
            elif self.bgPixels.getpixel((     clamp(round((playerPos +73) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height - 1)    )) == (255, 255, 255):
                self.grounded = True
            elif self.bgPixels.getpixel((     clamp(round((playerPos +57) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] - self.velocity / 2 * deltaTime)/3.75), 0, self.bgSizes.height -1)    )) == (255, 255, 255):
                self.grounded = True
            else:
                self.grounded = False
            if self.down == True and self.grounded == True:
                Clock.unschedule(self.moveAnimation)
                self.down = False
                self.animationFrame = 16
                Clock.schedule_interval(self.downAnimation, 1/30)
                self.settleSfx.play()
            if self.up == True and self.grounded == True:
                self.velocity = self.jumpHeight
        elif self.up == True:
            self.up = False
            self.animationFrame = -1
            Clock.schedule_interval(self.upAnimation, 1/30)
            self.riseSfx.play()

        # More Collisions yay! (this time on the top)
        if self.velocity * deltaTime > 0 and self.bgPixels.getpixel((     clamp(round((playerPos +73) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 102)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0) and self.bgPixels.getpixel((     clamp(round((playerPos +41) / 3.75), 0, self.bgSizes.width),    clamp(round(self.bgSizes.height - (self.player.pos[1] + self.velocity * deltaTime + 102)/3.75), 0, self.bgSizes.height -1)    )) == (0, 0, 0):
            self.player.pos[1] += self.velocity * deltaTime
        elif self.velocity * deltaTime > 0:
            self.velocity = 0
        else:
            self.player.pos[1] += self.velocity * deltaTime

        # Guard positions, visibility and movement
        bgPos = self.bg.pos[0]
        for i in range(0, len(self.enemy)):
            self.warningCircle[i].center_x = self.enemy[i].pos[0] + 25
            self.warningCircle[i].center_y = self.enemy[i].center_y
            enemyPos = bgPos + lerp(self.enemyX0[i], self.enemyX1[i], (m.sin((Clock.get_boottime() + i**2) / max(abs(self.enemyX0[i] - self.enemyX1[i]) / 100, 0.1)) +1) /2)
            trueEnemyPos = lerp(self.enemyX0[i], self.enemyX1[i], (m.sin((Clock.get_boottime() + i**2) / max(abs(self.enemyX0[i] - self.enemyX1[i]) / 100, 0.1)) +1) /2)
            
            if trueEnemyPos - self.prevEnemyPos[i] < 0:
                self.enemy[i].source = "./animations/sprite_1_" + str(min(round(self.enemyFrame[i]), 9)) + ".png"
                self.enemy[i].texture.mag_filter = "nearest"
                if self.enemyFrame[i] < 9:
                    self.enemyFrame[i] +=10 * deltaTime
                else:
                    self.enemyFrame[i] = 0
            elif trueEnemyPos - self.prevEnemyPos[i] > 0:
                self.enemy[i].source = "./animations/sprite_0_" + str(min(round(self.enemyFrame[i]), 9)) + ".png"
                self.enemy[i].texture.mag_filter = "nearest"
                if self.enemyFrame[i] < 9:
                    self.enemyFrame[i] +=10 * deltaTime
                else:
                    self.enemyFrame[i] = 0

            if not self.warning[i] == None:
                self.warning[i].pos[0] = self.enemy[i].pos[0] - 25
                self.warning[i].pos[1] = self.enemy[i].top - 50
            
            self.enemy[i].pos[0] = enemyPos
            self.prevEnemyPos[i] = trueEnemyPos

            #Sightseeing
            distanceFromEnemy = m.sqrt((self.player.center_x - (self.enemy[i].pos[0] + 25))**2 + (self.player.center_y - self.enemy[i].center_y)**2)
            if self.movable and distanceFromEnemy < self.loseLength:
                self.bg.pos[0] = -350
                self.player.pos[1] = 215
                self.playerWarned[i] = False
                self.remove_widget(self.warning[i])
                self.warning[i] = None

            if distanceFromEnemy < self.hitLength:
                lineDir = (self.enemy[i].pos[0] - self.player.center_x, self.enemy[i].center_y - self.player.center_y)
                lineDirNorm = (1/distanceFromEnemy * lineDir[0], 1/distanceFromEnemy * lineDir[1])
                for b in range(0, round(distanceFromEnemy/3.75)):
                    playerCaught = True
                    if self.bgPixels.getpixel((round((self.player.center_x - bgPos + lineDirNorm[0] * b*3.75)/3.75), round(self.bgCollisions.height - (self.player.center_y + lineDirNorm[1] * b*3.75)/3.75))) == (255, 255, 255):
                        playerCaught = False
                        break
                if not self.movable:
                    playerCaught = False
                if playerCaught or self.playerWarned[i]:
                    if self.playerWarned[i] == True and self.warning[i] == None and not self.checkScheduled[i]:
                        self.warning2.play()
                        self.warning[i] = Image(source="redWarning.png", width=dp(100), height=dp(100))
                        self.warning[i].pos[0] = self.enemy[i].pos[0] - 25
                        self.warning[i].pos[1] = self.enemy[i].top - 50
                        self.add_widget(self.warning[i])
                        self.checkScheduled[i] = True
                        Clock.schedule_once(partial(self.endCatch, i), 1.5)
                    elif self.warning[i] == None and not self.playerWarned[i] == True and not self.checkScheduled[i]:
                        self.warning1.play()
                        self.warning[i] = Image(source="yellowWarning.png", width=dp(100), height=dp(100))
                        self.warning[i].pos[0] = self.enemy[i].pos[0] - 25
                        self.warning[i].pos[1] = self.enemy[i].top - 50
                        self.add_widget(self.warning[i])
                        self.checkScheduled[i] = True
                        Clock.schedule_once(partial(self.timedCatch, i), 1.5)

        if -self.bg.pos[0] > 8100 and self.player.center_y > 430:
            self.youWon = Image(source="youWon.png", width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])
            self.add_widget(self.youWon)
            Clock.schedule_once(self.endGame, 1)
            
    def timedCatch(self, enemy, dt):
        if self.movable:
            bgPos = self.bg.pos[0]
            distanceFromEnemy = m.sqrt((self.player.center_x - (self.enemy[enemy].pos[0] + 25))**2 + (self.player.center_y - self.enemy[enemy].center_y)**2)
            if distanceFromEnemy < self.hitLength:
                lineDir = (self.enemy[enemy].pos[0] - self.player.center_x, self.enemy[enemy].center_y - self.player.center_y)
                lineDirNorm = (1/distanceFromEnemy * lineDir[0], 1/distanceFromEnemy * lineDir[1])
                for b in range(0, round(distanceFromEnemy/3.75)):
                    playerCaught = True
                    if self.bgPixels.getpixel((round((self.player.center_x - bgPos + lineDirNorm[0] * b*3.75)/3.75), round(self.bgCollisions.height - (self.player.center_y + lineDirNorm[1] * b*3.75)/3.75))) == (255, 255, 255):
                        playerCaught = False
                        break
                if playerCaught == True:
                    self.playerWarned[enemy] = True
                    self.remove_widget(self.warning[enemy])
                    self.warning[enemy] = None
                else:
                    self.remove_widget(self.warning[enemy])
                    self.warning[enemy] = None
            else:
                self.remove_widget(self.warning[enemy])
                self.warning[enemy] = None
        else:
            self.remove_widget(self.warning[enemy])
            self.warning[enemy] = None

        self.checkScheduled[enemy] = False

    def endCatch(self, enemy, dt):
        if self.movable:
            bgPos = self.bg.pos[0]
            distanceFromEnemy = m.sqrt((self.player.center_x - (self.enemy[enemy].pos[0] + 25))**2 + (self.player.center_y - self.enemy[enemy].center_y)**2)
            if distanceFromEnemy < self.hitLength:
                lineDir = (self.enemy[enemy].pos[0] - self.player.center_x, self.enemy[enemy].center_y - self.player.center_y)
                lineDirNorm = (1/distanceFromEnemy * lineDir[0], 1/distanceFromEnemy * lineDir[1])
                for b in range(0, round(distanceFromEnemy/3.75)):
                    playerCaught = True
                    if self.bgPixels.getpixel((round((self.player.center_x - bgPos + lineDirNorm[0] * b*3.75)/3.75), round(self.bgCollisions.height - (self.player.center_y + lineDirNorm[1] * b*3.75)/3.75))) == (255, 255, 255):
                        playerCaught = False
                        break
                if playerCaught == True:
                    self.warning3.play()
                    self.bg.pos[0] = -350
                    self.player.pos[1] = 215
                    self.playerWarned[enemy] = False
                    self.remove_widget(self.warning[enemy])
                    self.warning[enemy] = None
                else:
                    self.playerWarned[enemy] = False
                    self.remove_widget(self.warning[enemy])
                    self.warning[enemy] = None
            else:
                self.playerWarned[enemy] = False
                self.remove_widget(self.warning[enemy])
                self.warning[enemy] = None 
        else:
            self.playerWarned[enemy] = False
            self.remove_widget(self.warning[enemy])
            self.warning[enemy] = None 

        self.checkScheduled[enemy] = False

    def upAnimation(self, deltaTime):
        self.animationFrame += 1
        self.player.source = "./animations/player_0_" + str(self.animationFrame) + ".png"
        self.player.texture.mag_filter = "nearest"
        if self.animationFrame >=15:
            self.movable = True
            Clock.unschedule(self.upAnimation)
            self.animationFrame = 11
            Clock.schedule_interval(self.moveAnimation, 1/30)
            Clock.schedule_interval(self.hoverSound, self.hoverSfx.length - 0.1)

    def downAnimation(self, deltaTime):
        try:
            Clock.unschedule(self.hoverSound)
        except:
            pass
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

    def hoverSound(self, dt):
        self.hoverSfx.play()
    
    def playSong(self, dt):
        self.gameSong.play()
            
    def endGame(self, dt):
        App.get_running_app().stop()

class MainApp(App):
    pass

if __name__ == "__main__":
    MainApp().run()
