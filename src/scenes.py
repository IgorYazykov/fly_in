import pygame
from typing import Any
from .structures import MenuGeneral


class MenuDirectori(MenuGeneral):
	def take_data(self):
		self.fileOperator.dir_finder()
		self.names = self.fileOperator.take_names()
		self.links = self.fileOperator.take_levels()

	def update_metric(self, width: int, height: int):
		self.list_rect.clear()
		self.list_sur_text.clear()
		self.list_text_rect.clear()
		block_w = int(width * 0.35)
		block_h = int(height * 0.12)
		spacing = int(height * 0.045)
		font_size = int(block_h * 0.55)
		midl_h = height // 2
		midl_w = width // 2
		total_buttons = len(self.names)
		total_menu_h = ((block_h + spacing) * total_buttons - spacing)
		start_y = midl_h - (total_menu_h // 2)
		start_x = midl_w - (block_w // 2)
		font = pygame.font.SysFont("Arial", font_size)

		for i in range(total_buttons):
			bottom_mar = start_y + ((spacing + block_h) * i)
			rect = pygame.Rect(start_x, bottom_mar, block_w, block_h)
			self.list_rect.append(rect)

			sur_text = font.render(self.names[i], True, "white")
			text_rect = sur_text.get_rect(center = (
				start_x + block_w // 2,
				bottom_mar + block_h // 2
			))
			self.list_sur_text.append(sur_text)
			self.list_text_rect.append(text_rect)

	def draw_menu(self, surface: pygame.Surface):
		surface.fill((20, 20, 40))
		for i in range(len(self.names)):
			pygame.draw.rect(
				surface,
				"darkolivegreen",
				self.list_rect[i],
				border_radius=10)
			surface.blit(
				self.list_sur_text[i],
				self.list_text_rect[i])

	def handle_click(self, mouse_pos: tuple[int, int]) -> Any | None:
		for i in range(len(self.list_rect)):
			if self.list_rect[i].collidepoint(mouse_pos):
				return(self.links[i])
		return None
		

class MenuTXT(MenuGeneral):
	def __init__(self, target_dir: Any):
		super().__init__()
		self.target_dir: Any = target_dir
		self.scroll_y: int = 0
		self.max_scroll: int = 0
		self.scroll_box = pygame.Rect(0, 0, 0, 0)
		self.font_size: int
		self.button_back = pygame.Rect(0, 0, 0, 0)

	def take_data(self):
		self.fileOperator.txt_finder(self.target_dir)
		self.names = self.fileOperator.take_name_maps()
		self.links = self.fileOperator.take_maps()

	def update_metric(self, width: int, height: int):
		self.list_rect.clear()
		self.list_sur_text.clear()
		self.list_text_rect.clear()
		block_w = int(width * 0.18)
		block_h = int(height * 0.1)
		spacing_x = int(width * 0.03)
		spacing_y = int(height * 0.04)
		self.font_size = int(block_h * 0.2)
		midl_h = height // 2
		midl_w = width // 2
		colums = 3

		# Calculeting of size of all table
		total_box_w = ((block_w + spacing_x) * colums + spacing_x)
		total_box_h = ((block_h + spacing_y) * 4 + spacing_y)

		# Calculate of beginig position of menu
		box_start_x = midl_w - (total_box_w // 2)
		box_start_y = midl_h - (total_box_h // 2)

		self.scroll_box = pygame.Rect(box_start_x, box_start_y, total_box_w, total_box_h)

		self.button_back = pygame.Rect(
			(box_start_x + (total_box_w // 2) - (block_w//2)),
			(total_box_h + box_start_y + spacing_y),
			block_w,
			block_h
		)

		for i in range(len(self.names)):
			# Put buttons for column and lines 
			col = i % colums
			row = i // colums

			bx = box_start_x + spacing_x + col * (block_w + spacing_x)
			by = box_start_y + spacing_y + row * (block_h + spacing_y)

			self.list_rect.append(pygame.Rect(bx, by, block_w, block_h))

		if self.list_rect:
			total_content_h = self.list_rect[-1].bottom - box_start_y
			#Calculate of maximum of scrolling
			self.max_scroll = max(0, total_content_h - self.scroll_box.height + spacing_y)
			self.scroll_y = min(self.scroll_y, self.max_scroll)

	def handle_scroll_up(self):
		self.scroll_y = max(0, self.scroll_y - 30)

	def handle_scroll_down(self):
		self.scroll_y = min(self.max_scroll, self.scroll_y + 30)

	def draw_menu(self, surface: pygame.Surface):
		surface.fill("darkslategray")

		font = pygame.font.SysFont("Arial", self.font_size)

		pygame.draw.rect(surface, "gold", self.button_back, border_radius=15)
		sur_text = font.render("Back", True, "white")
		text_rect = sur_text.get_rect(center=self.button_back.center)
		surface.blit(sur_text, text_rect)
		
		pygame.draw.rect(surface, "forestgreen", self.scroll_box, border_radius=15)
		surface.set_clip(self.scroll_box)
		# mouse_pos = pygame.mouse.get_pos()

		for i in range(len(self.list_rect)):
			moved_rect = self.list_rect[i].copy()
			moved_rect.y -= self.scroll_y

			pygame.draw.rect(surface, "goldenrod", moved_rect, border_radius=5)
			sur_text = font.render(self.names[i], True, "white")
			text_rect = sur_text.get_rect(center=moved_rect.center)
			surface.blit(sur_text, text_rect)

		surface.set_clip(None)


	def handle_click(self, mouse_pos: tuple[int, int]) -> Any | None:
		if self.button_back.collidepoint(mouse_pos):
			return ("Back")
		else:
			if self.scroll_box.collidepoint(mouse_pos):
				for i in range(len(self.list_rect)):
					moved_rect = self.list_rect[i].copy()
					moved_rect.y -= self.scroll_y
					if moved_rect.collidepoint(mouse_pos):
						return (self.links[i])
		return None


class Animation():
	def pri(self):
		print('Animation')