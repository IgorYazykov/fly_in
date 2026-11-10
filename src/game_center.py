import pygame
from typing import Any
from .menu_scenes import MenuGeneral, MenuDirectori, MenuTXT
from .animation_scene import Animation
from .parser import Parser
from .structures import Nodes_holder


class GameCenter():
	def __init__(self):
		self.width = 1280
		self.height = 700
		self.scenes: dict = {
			"menu_dir": MenuDirectori,
			"menu_txt": MenuTXT,
			"animation": Animation
		}
		self.parser = Parser()
		self.current_scene: MenuDirectori | MenuTXT | Animation = self.scenes["menu_dir"]()
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

	def chenge_of_window(self, x: int, y: int):
		self.width = x
		self.height = y
		if isinstance(self.current_scene, MenuGeneral):
			self.current_scene.update_metric(self.width, self.height)
		elif isinstance(self.current_scene, Animation): 
			pass

	def change_scene(self, target_scene: str, data: Any = None):
		if data == None:
			self.current_scene = self.scenes[target_scene]()
		elif isinstance(data, Nodes_holder):
			self.current_scene = self.scenes[target_scene](data)
		else:
			self.current_scene = self.scenes[target_scene](data)

	def drawing_handeler(self, surface: pygame.Surface):
		if isinstance(self.current_scene, MenuGeneral):
			self.current_scene.draw_menu(surface)
		if isinstance(self.current_scene, Animation):
			self.current_scene.draw_menu(surface)

	def game_click_handeler(self, mouse_pos: tuple[int, int]):
		if isinstance(self.current_scene, MenuDirectori):
			res = self.current_scene.handle_click(mouse_pos)
			if res != None:
				self.change_scene('menu_txt', res)
				self.current_scene.take_data()
				self.current_scene.update_metric(self.width, self.height)
		elif isinstance(self.current_scene, MenuTXT):
			res = self.current_scene.handle_click(mouse_pos)
			if res == "Back":
				self.change_scene('menu_dir')
				self.current_scene.take_data()
				self.current_scene.update_metric(self.width, self.height)
			elif res != None:
				if self.parser.file_checker(res) == 1:
					pass
				else:
					node_map = self.parser.get_map()
					self.change_scene('animation', node_map)
					if (self.current_scene.init_img() == 1):
						self.current_scene = self.scenes["menu_dir"]()
					else:
						self.current_scene.update_metric(self.width, self.height)

	def main_loop(self):
		pygame.init()
		clock = pygame.time.Clock()
		running = True
		self.current_scene.take_data()
		self.current_scene.update_metric(self.width, self.height)
		sys_window = pygame.Window.from_display_module()
		sys_window.minimum_size = (900, 600)
	
		while running:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.WINDOWRESIZED:
					self.chenge_of_window(event.x, event.y)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						self.game_click_handeler(event.pos)
					if (isinstance(self.current_scene, MenuTXT)
					    and event.button == 4):
						self.current_scene.handle_scroll_up()
					if (isinstance(self.current_scene, MenuTXT)
					    and event.button == 5):
						self.current_scene.handle_scroll_down()

			self.screen.fill((30, 30, 30))
			self.drawing_handeler(self.screen)
			pygame.display.flip()
		pygame.quit()