import pygame


class MenuDirectori():
	def pri(self):
		print('Menu dir')


class MenuTXT():
	def pri(self):
		print('Menu txt')


class Animation():
	def pri(self):
		print('Animation')


class GameCenter():
	def __init__(self):
		self.scenes: dict = {
			"menu_dir": MenuDirectori,
			"menu_txt": MenuTXT,
			"animation": Animation
		}
		self.current_scene: MenuDirectori | MenuTXT | Animation = self.scenes["menu_dir"]()

	def main_loop(self):
		pygame.init()
		screen = pygame.display.set_mode((1280, 700))
		clock = pygame.time.Clock()
		running = True
	
		while running:
			pygame.display.flip()
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					if event == pygame.K_UP:
						self.current_scene = self.scenes["menu_dir"]()
					if event == pygame.K_LEFT:
						self.current_scene = self.scenes["menu_txt"]()
					if event == pygame.K_RIGHT:
						self.current_scene = self.scenes["animation"]()
			self.current_scene.pri()
		pygame.quit()