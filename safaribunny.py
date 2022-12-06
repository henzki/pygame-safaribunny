import pygame
from pygame.locals import *
from pygame import mixer

import pickle
from os import path

from models.platforms import *
from models.enemies import *
from models.carrots import *

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

# Screen settings
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Safari Bunny')

# Font
font = pygame.font.SysFont('Comic Sans MS', 50, bold=True)
font_score = pygame.font.SysFont('Comic Sans MS', 20)
font_bold = pygame.font.SysFont('Comic Sans MS', 24, bold=True)
font_henzki = pygame.font.SysFont('Comic Sans MS', 17)
font_small = pygame.font.SysFont('Arial', 11)
font_total = pygame.font.SysFont('Comic Sans MS', 35, bold=True)

# Colors palette
violet = (148,88,172)
lila = (190,117,228)
brown = (97,67,5,255)
beige = (236,222,188,255)

# Images
bg_img = pygame.image.load('images/colored_desert.png')
safaribunny_img = pygame.image.load('images/safaribunny.png')
bunny_start_img = pygame.image.load('images/bunny_start.png')
bunny_start_img = pygame.transform.scale(bunny_start_img, (100, 115))
start_img = pygame.image.load('images/start.png')
start_img = pygame.transform.scale(start_img, (260, 260))
restart_img = pygame.image.load('images/reload.png')
restart_img = pygame.transform.scale(restart_img, (100, 100))
finish_img = pygame.image.load('images/carrot_gold.png')
finish_img = pygame.transform.scale(finish_img, (50, 50))
exit_img = pygame.image.load('images/exit.png')
exit_img = pygame.transform.scale(exit_img, (100, 100))
heart_img = pygame.image.load('images/heart.png')
heart_img = pygame.transform.scale(heart_img, (16, 16))

# Icon
pygame.display.set_icon(bunny_start_img)

# Sounds
pygame.mixer.music.load('sounds/music-loop.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

jump_sound = pygame.mixer.Sound('sounds/jump.wav')
jump_sound.set_volume(1)

carrot_sound = pygame.mixer.Sound('sounds/carrot.wav')
carrot_sound.set_volume(1)

win_sound = pygame.mixer.Sound('sounds/game-win.wav')
win_sound.set_volume(2)

# Variables
start_menu = True
tile_size = 50
level = 0
max_levels = 10
score = 0
game_over = 0

# Draw text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Reset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    spikeman_group.empty()
    platform_group.empty()
    lava_group.empty()
    finish_group.empty()
    bat_group.empty()
    cakeplatform_group.empty()
    tundraplatform_group.empty()
    spikes_group.empty()
    barnacle_group.empty()
    snail_group.empty()
    if path.exists(f'./levels/level{level}'):
        pickle_in = open(f'./levels/level{level}', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Mouse position and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        # Variables
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20
        
        if game_over == 0:
        # Keypresses
            key = pygame.key.get_pressed()
            # Jump
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_sound.play()
                self.speed_y = -20
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            # Go left
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            # Go right
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Animation
            if self.counter > walk_cooldown:
                self.counter = 0    
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Gravity
            self.speed_y += 1
            if self.speed_y > 10:
                self.speed_y = 10
            dy += self.speed_y

            # Collision
            self.in_air = True
            for tile in world.tile_list:
                # X direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below ground, jumping
                    if self.speed_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.speed_y = 0
                    # Check if above ground, jumping
                    elif self.speed_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.speed_y = 0
                        self.in_air = False
                        
            # Collision with finish
            if pygame.sprite.spritecollide(self, finish_group, False):
                game_over = 1

            # Collision with enemies
            if pygame.sprite.spritecollide(self, spikeman_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, bat_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, spikes_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, barnacle_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, snail_group, False):
                game_over = -1

            # Collision with platforms
            for platform in platform_group:
                # X direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Below
                    if abs((self.rect.top) + dy - platform.rect.bottom) < col_thresh:
                        self.speed_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # Above
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top -1
                        self.in_air = False
                        dy = 0
                    # Move sideways with platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            for cakeplatform in cakeplatform_group:
                # X direction
                if cakeplatform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Y direction
                if cakeplatform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Below
                    if abs((self.rect.top) + dy - cakeplatform.rect.bottom) < col_thresh:
                        self.speed_y = 0
                        dy = cakeplatform.rect.bottom - self.rect.top
                    # Above
                    elif abs((self.rect.bottom + dy) - cakeplatform.rect.top) < col_thresh:
                        self.rect.bottom = cakeplatform.rect.top -1
                        self.in_air = False
                        dy = 0
                    # Move sideways with cakeplatform
                    if cakeplatform.move_x != 0:
                        self.rect.x += cakeplatform.move_direction
            
            for tundraplatform in tundraplatform_group:
                # X direction
                if tundraplatform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Y direction
                if tundraplatform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Below
                    if abs((self.rect.top) + dy - tundraplatform.rect.bottom) < col_thresh:
                        self.speed_y = 0
                        dy = tundraplatform.rect.bottom - self.rect.top
                    # Above
                    elif abs((self.rect.bottom + dy) - tundraplatform.rect.top) < col_thresh:
                        self.rect.bottom = tundraplatform.rect.top -1
                        self.in_air = False
                        dy = 0
                    # Move sideways with tundraplatform
                    if tundraplatform.move_x != 0:
                        self.rect.x += tundraplatform.move_direction

            self.rect.x += dx
            self.rect.y += dy

        # Update game over; player image and text
        elif game_over == -1:
            self.image = self.hurt_image
            draw_text('GAME OVER', font, violet, (screen_width // 2) - 150, 330)

        screen.blit(self.image, self.rect)

        return game_over
    
    # Update player images
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'images/bunny_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.hurt_image = pygame.image.load('images/bunny_hurt.png')
        self.hurt_image = pygame.transform.scale(self.hurt_image, (45, 80))
        self.image = self.images_right[self.index]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 0
        self.direction = 0
        self.jumped = False
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        # Images
        sandCenter_img = pygame.image.load('images/sandCenter.png')
        sand_img = pygame.image.load('images/sand.png')
        cakeCenter_img = pygame.image.load('images/cakeCenter.png')
        cake_img = pygame.image.load('images/cake.png')
        tundraCenter_img = pygame.image.load('images/tundraCenter.png')
        tundra_img = pygame.image.load('images/tundra.png')

        # Determine numbers for tiles
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # Sand center
                if tile == 1:
                    img = pygame.transform.scale(sandCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Sand
                if tile == 2:
                    img = pygame.transform.scale(sand_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Spikeman
                if tile == 3:
                    spikeman = Spikeman(col_count * tile_size, row_count * tile_size)
                    spikeman_group.add(spikeman)
                # Horizontally moving platform
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                # Vertically moving platform - smaller image size
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                # Lava
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                # Carrot
                if tile == 7:
                    carrot = Carrot(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    carrot_group.add(carrot)
                # Finish
                if tile == 8:
                    finish = Finish(col_count * tile_size, row_count * tile_size)
                    finish_group.add(finish)
                # Bat
                if tile == 9:
                    bat = Bat(col_count * tile_size, row_count * tile_size + 10)
                    bat_group.add(bat)
                # Cake center
                if tile == 10:
                    img = pygame.transform.scale(cakeCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Cake
                if tile == 11:
                    img = pygame.transform.scale(cake_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Tundra center
                if tile == 12:
                    img = pygame.transform.scale(tundraCenter_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Tundra
                if tile == 13:
                    img = pygame.transform.scale(tundra_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Horizontally moving cakeplatform
                if tile == 14:
                    cakeplatform = CakePlatform(col_count * tile_size, row_count * tile_size, 1, 0)
                    cakeplatform_group.add(cakeplatform)
                # Vertically moving cakeplatform
                if tile == 15:
                    cakeplatform = CakePlatform(col_count * tile_size, row_count * tile_size, 0, 1)
                    cakeplatform_group.add(cakeplatform)
                # Horizontally moving tundraplatform
                if tile == 16:
                    tundraplatform = TundraPlatform(col_count * tile_size, row_count * tile_size, 1, 0)
                    tundraplatform_group.add(tundraplatform)
                # Vertically moving tundraplatform
                if tile == 17:
                    tundraplatform = TundraPlatform(col_count * tile_size, row_count * tile_size, 0, 1)
                    tundraplatform_group.add(tundraplatform)
                # Spikes
                if tile == 18:
                    spikes = Spikes(col_count * tile_size, row_count * tile_size)
                    spikes_group.add(spikes)
                # Barnacle
                if tile == 19:
                    barnacle = Barnacle(col_count * tile_size, row_count * tile_size)
                    barnacle_group.add(barnacle)
                # Snail
                if tile == 20:
                    snail = Snail(col_count * tile_size, row_count * tile_size + 20)
                    snail_group.add(snail)
                
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# Instances
player = Player(100, screen_height - 130)

spikeman_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
carrot_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()
cakeplatform_group = pygame.sprite.Group()
tundraplatform_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
barnacle_group = pygame.sprite.Group()
snail_group = pygame.sprite.Group()

# Carrot image for score
score_carrot = Carrot(tile_size // 2, tile_size // 2)
carrot_group.add(score_carrot)

# Level data load
if path.exists(f'levels/level{level}'):
    pickle_in = open(f'levels/level{level}', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# Buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 50, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2 + 50, start_img)
finish_button = Button(screen_width // 2 + 220, screen_height // 2 + 80, exit_img)

run = True
while run:

    clock.tick(fps)

    # Background image
    screen.blit(bg_img, (0, 0))

    # Starting menu
    if start_menu == True:
        screen.blit(safaribunny_img, ((screen_width // 2) - 392, 200))
        screen.blit(bunny_start_img, ((screen_width // 2) - 55, 230))
        screen.blit(heart_img, ((screen_width // 2) - 45, screen_height // 2 + 450))
        draw_text('henzki', font_henzki, violet, screen_width // 2 - 23, screen_height // 2 + 446)
        draw_text('Images: Kenney, https://opengameart.org', font_small, brown, screen_width // 2 - 80, screen_height // 2 + 468)
        draw_text('Icons: Flaticon, Start icons created by Good Ware, finish icons created by Freepik and Heart icons created by Vectors Market', font_small, brown, screen_width // 2 - 270, screen_height // 2 + 480)
        if finish_button.draw():
            run = False
        if start_button.draw():
            start_menu = False
    else:
        world.draw()

        if game_over == 0:
            # Stop movement
            spikeman_group.update()
            platform_group.update()
            bat_group.update()
            barnacle_group.update()
            snail_group.update()
            cakeplatform_group.update()
            tundraplatform_group.update()

            # Update score
            if pygame.sprite.spritecollide(player, carrot_group, True):
                score += 1
                carrot_sound.play()
            draw_text('x ' + str(score), font_score, beige, tile_size, 10)
            draw_text('Level: ' + str(level), font_bold, lila, screen_width // 2 - 50, 60)

        # Draw on screen
        spikeman_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        carrot_group.draw(screen)
        finish_group.draw(screen)
        bat_group.draw(screen)
        cakeplatform_group.draw(screen)
        tundraplatform_group.draw(screen)
        spikes_group.draw(screen)
        barnacle_group.draw(screen)
        snail_group.draw(screen)
        
        game_over = player.update(game_over)

        # Player lost
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        
        # Player won
        if game_over == 1:
            win_sound.play()
            # Go to next lever
            level += 1
            if level <= max_levels:
                # Reset the level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                screen.blit(finish_img, ((screen_width // 2) - 190, 260))
                screen.blit(finish_img, ((screen_width // 2) + 150, 260))
                draw_text('YOU WIN', font, violet, (screen_width // 2) - 120, 250)
                draw_text('Your score: ' + str(score), font_total, violet, (screen_width // 2) - 110, 330)
                # Restart the game
                if restart_button.draw():
                    level = 0
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        # Quitting the game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()