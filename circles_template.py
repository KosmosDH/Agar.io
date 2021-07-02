import arcade
import random

# задаем ширину, высоту и заголовок окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Circle Game"


class Circle(arcade.Sprite):
    def __init__(self, scale):
        super().__init__("circle.png", scale)
        sides = ["left", "top", "right", "bottom"]
        self.side = random.choice(sides)
        if self.side == "left":
            self.right = 0
            self.center_y = random.randint(0, SCREEN_HEIGHT)
            self.change_x = random.uniform(2, 5)
            self.change_y = random.uniform(-3, -2)
        elif self.side == "right":
            self.left = SCREEN_WIDTH
            self.center_y = random.randint(0, SCREEN_HEIGHT)
            self.change_x = random.uniform(-3, -2)
            self.change_y = random.uniform(-3, -2)
        elif self.side == "top":
            self.bottom = SCREEN_HEIGHT
            self.center_x = random.randint(0, SCREEN_WIDTH)
            self.change_x = random.uniform(-3, -2)
            self.change_y = random.uniform(-5, -2)
        elif self.side == "bottom":
            self.top = 0
            self.center_x = random.randint(0, SCREEN_WIDTH)
            self.change_x = random.uniform(-3, -2)
            self.change_y = random.uniform(2, 3)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.side == "left" and (self.left >= SCREEN_WIDTH or self.top <= 0):
            self.kill()
        elif self.side == "right" and (self.right <= 0 or self.top <= 0):
            self.kill()
        elif self.side == "top" and (self.top <= 0 or self.right <= 0):
            self.kill()
        elif self.side == "bottom" and (self.bottom >= SCREEN_HEIGHT or self.right <= 0):
            self.kill()


class OurGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.circles = arcade.SpriteList()

    # начальные значения
    def setup(self):
        for i in range(30):
            circle = Circle(1)
            self.circles.append(circle)

    # отрисовка объектов
    def on_draw(self):
        arcade.start_render()
        self.circles.draw()

    # логика
    def update(self, delta_time):
        self.circles.update()
        while len(self.circles) < 30:
            circle = Circle(1)
            self.circles.append(circle)


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
# цвета от 50 - 200, размеры, класс игрока (коф.сж. - (0.3 - 0.4))
