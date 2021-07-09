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
        self.color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )
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


class Player(Circle):
    def __init__(self):
        super().__init__(0.3)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0
        self.color = arcade.color.WHITE


class OurGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen= True)
        global SCREEN_WIDTH, SCREEN_HEIGHT
        self.circles = arcade.SpriteList()
        self.player = None
        self.sound = arcade.load_sound("Drip Drop.wav")
        screen_width, screen_height = self.get_viewport_size()
        SCREEN_WIDTH, SCREEN_HEIGHT = screen_width, screen_height
        self.game = True
        self.exit = False

    # начальные значения
    def setup(self):
        if self.game:
            self.music = arcade.play_sound(self.sound, volume= 0.5)
            self.player = Player()
            for i in range(50):
                circle = Circle(random.uniform(0.1, self.player.scale + 0.5))
                self.circles.append(circle)

    # отрисовка объектов
    def on_draw(self):
        arcade.start_render()
        self.circles.draw()
        self.player.draw()
        if not self.game:
            arcade.draw_text("PAUSE", SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, arcade.color.WHITE, 20)

    # логика
    def update(self, delta_time):
        if self.game:
            self.circles.update()
            self.player.update()
            collisions = arcade.check_for_collision_with_list(self.player, self.circles)
            if len(collisions) > 0:
                for circle in collisions:
                    if circle.scale > self.player.scale:
                        exit()
                    else:
                        circle.kill()
                        self.player.scale += 0.01
                        if self.player.scale >= 2:
                            exit()
            if self.sound.get_stream_position(self.music) == 0:
                self.music = arcade.play_sound(self.sound, volume= 0.5)
            while len(self.circles) < 30:
                circle = Circle(random.uniform(0.1, self.player.scale + 0.5))
                self.circles.append(circle)
            if self.exit:
                exit()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.game = False
        if symbol == arcade.key.LSHIFT:
            self.game = True
        if symbol == arcade.key.ESCAPE and self.game:
            self.exit = True

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.game:
            self.player.center_x = x
            self.player.center_y = y


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
# TODO сделать паузу
