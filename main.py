import pygame as pg
import random

pg.init()

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 760
FPS = 80
GRAVITY = 1
JUMP_SPEED = -12
PIPE_SPEED = 6

PIPE_GAP = 250
PIPE_SPAWN_TIME = 1500

font = pg.font.Font(None, 40)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_animations()

        self.current_animation = self.idle_animation_right
        self.current_image = 0
        self.image = self.current_animation[self.current_image]
        self.rect = self.image.get_rect(center=(200, SCREEN_HEIGHT // 2))

        self.velocity_y = 0
        self.timer = pg.time.get_ticks()
        self.interval = 120
        self.alive = True

    def load_animations(self):
        tile_size = 16
        tile_scale = 3
        spritesheet = pg.image.load("Flappy Bird Assets/Player/StyleBird2/Bird2-1.png")

        self.idle_animation_right = []
        for i in range(4):
            rect = pg.Rect(i * tile_size, 0, tile_size, tile_size)
            frame = spritesheet.subsurface(rect)
            frame = pg.transform.scale(frame, (tile_size * tile_scale, tile_size * tile_scale))
            self.idle_animation_right.append(frame)

    def flap(self):
        if self.alive:
            self.velocity_y = JUMP_SPEED

    def animate(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image = (self.current_image + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def update(self):
        if self.alive:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

            if self.rect.top < 0:
                self.rect.top = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.alive = False

        self.animate()


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        image = pg.image.load("Flappy Bird Assets/Tiles/Style 1/PipeStyle1.png")
        image = pg.transform.scale(image, (100, 600))

        if flipped:
            self.image = pg.transform.flip(image, False, True)
            self.rect = self.image.get_rect(midbottom=(x, y - PIPE_GAP // 2))
        else:
            self.image = image
            self.rect = self.image.get_rect(midtop=(x, y + PIPE_GAP // 2))

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Flappy Bird")

        self.background = pg.image.load("Flappy Bird Assets/Background/Background6.png")
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True

        self.pipe_timer = 0

        self.start_time = pg.time.get_ticks()
        self.last_speed_increase = 0

        self.setup()

    def setup(self):
        global PIPE_SPEED, GRAVITY

        PIPE_SPEED = 6
        GRAVITY = 1

        self.player = Player()

        self.all_sprites = pg.sprite.Group()
        self.pipes = pg.sprite.Group()

        self.all_sprites.add(self.player)

        self.game_over = False
        self.start_time = pg.time.get_ticks()
        self.last_speed_increase = 0

    def spawn_pipes(self):
        y = random.randint(200, SCREEN_HEIGHT - 200)
        pipe_top = Pipe(SCREEN_WIDTH + 50, y, flipped=True)
        pipe_bottom = Pipe(SCREEN_WIDTH + 50, y, flipped=False)

        self.pipes.add(pipe_top, pipe_bottom)
        self.all_sprites.add(pipe_top, pipe_bottom)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if not self.game_over:
                    self.player.flap()
                else:
                    self.setup()

    def update_speed(self):
        global PIPE_SPEED, GRAVITY

        time = (pg.time.get_ticks() - self.start_time) // 1000

        if time // 10 > self.last_speed_increase:
            self.last_speed_increase = time // 10

            PIPE_SPEED += 1
            GRAVITY += 0.2

    def update(self):
        if not self.game_over:
            self.all_sprites.update()

            self.update_speed()

            if pg.time.get_ticks() - self.pipe_timer > PIPE_SPAWN_TIME:
                self.spawn_pipes()
                self.pipe_timer = pg.time.get_ticks()

            if pg.sprite.spritecollide(self.player, self.pipes, False):
                self.game_over = True
                self.player.alive = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)

        time = (pg.time.get_ticks() - self.start_time) // 1000
        time_text = font.render(f"Время: {time}", True, (255, 255, 255))
        self.screen.blit(time_text, (20, 20))

        if self.game_over:
            text = font.render("Вы проиграли", True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200))

        pg.display.flip()



if __name__ == "__main__":
    game = Game()
