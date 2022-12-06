import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Screen settings
tile_size = 50
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin
bunny_start_img = pygame.image.load('images/bunny_start.png')
pygame.display.set_icon(bunny_start_img)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# Images
bg_img = pygame.image.load('./images/colored_desert.png')
exit_img = pygame.image.load('./images/carrot_gold.png')
exit_img = pygame.transform.scale(exit_img, (140, 140))
sandCenter_img = pygame.image.load('./images/sandCenter.png')
sand_img = pygame.image.load('./images/sand.png')
cakeCenter_img = pygame.image.load('./images/cakeCenter.png')
cake_img = pygame.image.load('./images/cake.png')
tundraCenter_img = pygame.image.load('./images/tundraCenter.png')
tundra_img = pygame.image.load('./images/tundra.png')
spikeman_img = pygame.image.load('./images/spikeMan_stand.png')
bat_img = pygame.image.load('./images/bat_fly.png')
platform_img = pygame.image.load('./images/platform.png')
cakeplatform_img = pygame.image.load('./images/cakePlatform.png')
tundraplatform_img = pygame.image.load('./images/tundraPlatform.png')
lava_img = pygame.image.load('./images/lava.png')
spikes_img = pygame.image.load('./images/spikes.png')
barnacle_img = pygame.image.load('./images/barnacle.png')
snail_img = pygame.image.load('./images/snail.png')
carrot_img = pygame.image.load('./images/carrot.png')
save_img = pygame.image.load('./images/save.png')
save_img = pygame.transform.scale(save_img, (80, 80))
load_img = pygame.image.load('./images/load.png')
load_img  = pygame.transform.scale(load_img , (80, 80))

# Variables
clicked = False
level = 0

# Colours
white = (255, 255, 255)
beige = (205, 186, 150)
brown = (131, 94, 62, 1)

font = pygame.font.SysFont('Comic Sans MS', 16)

# Create empty
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

# Create boundary
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y): 
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Lines 
def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

# Determine numbers for tiles
def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				# Sand center
				if world_data[row][col] == 1:
					img = pygame.transform.scale(sandCenter_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Sand
				if world_data[row][col] == 2:
					img = pygame.transform.scale(sand_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Spikeman
				if world_data[row][col] == 3:
					img = pygame.transform.scale(spikeman_img, (int(tile_size * 0.75), int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size + (tile_size * 0.25), row * tile_size + (tile_size * 0.25)))
				# Horizontally moving platform
				if world_data[row][col] == 4:
					img = pygame.transform.scale(platform_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Vertically moving platform
				if world_data[row][col] == 5:
					img = pygame.transform.scale(platform_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Lava
				if world_data[row][col] == 6:
					img = pygame.transform.scale(lava_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Carrot
				if world_data[row][col] == 7:
					img = pygame.transform.scale(carrot_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				# Exit
				if world_data[row][col] == 8:
					img = pygame.transform.scale(exit_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Bat
				if world_data[row][col] == 9:
					img = pygame.transform.scale(bat_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				# Cake center
				if world_data[row][col] == 10:
					img = pygame.transform.scale(cakeCenter_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Cake
				if world_data[row][col] == 11:
					img = pygame.transform.scale(cake_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Tundra center
				if world_data[row][col] == 12:
					img = pygame.transform.scale(tundraCenter_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Tundra
				if world_data[row][col] == 13:
					img = pygame.transform.scale(tundra_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Horizontally moving cakeplatform
				if world_data[row][col] == 14:
					img = pygame.transform.scale(cakeplatform_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Vertically moving cakeplatform
				if world_data[row][col] == 15:
					img = pygame.transform.scale(cakeplatform_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Horizontally moving tundraplatform
				if world_data[row][col] == 16:
					img = pygame.transform.scale(tundraplatform_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Vertically moving tundraplatform
				if world_data[row][col] == 17:
					img = pygame.transform.scale(tundraplatform_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Spikes
				if world_data[row][col] == 18:
					img = pygame.transform.scale(spikes_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Barnacle
				if world_data[row][col] == 19:
					img = pygame.transform.scale(barnacle_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				# Snail
				if world_data[row][col] == 20:
					img = pygame.transform.scale(snail_img, (int(tile_size * 0.75), int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size + (tile_size * 0.25), row * tile_size + (tile_size * 0.25)))

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
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

		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

# Buttons
save_button = Button(screen_width // 2 - 100, screen_height - 75, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 75, load_img)

run = True
while run:

	clock.tick(fps)

	# Background
	screen.fill(beige)
	screen.blit(bg_img, (0, 0))

	# Load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'./levels/level{level}', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		# Load in level data
		if path.exists(f'./levels/level{level}'):
			pickle_in = open(f'./levels/level{level}', 'rb')
			world_data = pickle.load(pickle_in)


	# Show the grid and draw the level tiles
	draw_grid()
	draw_world()


	# Text showing current level
	draw_text(f'Level: {level}', font, brown, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, brown, tile_size, screen_height - 40)

	for event in pygame.event.get():
		# Quit game
		if event.type == pygame.QUIT:
			run = False
		# Mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			
			if x < 20 and y < 20:
				# Update tile
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 20:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 20
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		# Keypresses for level changing
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	pygame.display.update()

pygame.quit()