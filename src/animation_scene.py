from .structures import Nodes_holder, Node, ZoneType
import pygame


class Animation():
	def __init__(self, node_map):
		self.node_map_holder: Nodes_holder = node_map
		self.img_start_or: pygame.Surface | None = None
		self.img_end_or: pygame.Surface | None = None
		self.img_hub_norm_or: pygame.Surface | None = None
		self.img_hub_rest_or: pygame.Surface | None = None
		self.img_hub_prior_or: pygame.Surface | None = None
		self.img_hub_block_or: pygame.Surface | None = None
		self.img_start: pygame.Surface | None = None
		self.img_end: pygame.Surface | None = None
		self.img_hub_norm: pygame.Surface | None = None
		self.img_hub_rest: pygame.Surface | None = None
		self.img_hub_prior: pygame.Surface | None = None
		self.img_hub_block: pygame.Surface | None = None
		self.font = None
		self.node_map: list[Node] = []
		self.font_size: int = 0
		self.img_size: int = 0

	def init_img(self) -> int:
		try:
			self.img_start_or = pygame.image.load("src/img/start-png-44879.png")
			self.img_end_or = pygame.image.load("src/img/finished-png-33595.png")
			self.img_hub_norm_or = pygame.image.load("src/img/square-png-25133.png")
			self.img_hub_rest_or = pygame.image.load("src/img/triangle-png-42421.png")
			self.img_hub_prior_or = pygame.image.load("src/img/circle-png-25307.png")
			self.img_hub_block_or = pygame.image.load("src/img/image.png")
			self.node_map = self.node_map_holder.nodes.copy()
			self.node_map.append(self.node_map_holder.start)
			self.node_map.append(self.node_map_holder.end)
			return(0)
		except pygame.error as err:
			print(err)
			return(1)
		
	def update_metric(self, width: int, height: int):
		self.font_size = int(min(height, width) * 0.015)
		self.font = pygame.font.SysFont("Arial", self.font_size)

		min_cord_x = min(self.node_map, key=lambda node: node.x).x
		min_cord_y = min(self.node_map, key=lambda node: node.y).y
		max_cord_x = max(self.node_map, key=lambda node: node.x).x
		max_cord_y = max(self.node_map, key=lambda node: node.y).y

		numb_nodes_row = max_cord_x - min_cord_x + 1
		numb_nodes_col = max_cord_y - min_cord_y + 1

		margin_w = int(width * 0.013)
		margin_h = int(height * 0.012)
		
		size_node_w = int((width - (margin_w * (numb_nodes_row + 1))) / numb_nodes_row)
		size_node_h = int((height - (margin_h * (numb_nodes_col + 1))) / numb_nodes_col)

		self.img_size = min(size_node_h, size_node_w)

		gen_height_marg = int((height - (self.img_size * numb_nodes_col + margin_h * (numb_nodes_col - 1)))/2)
		gen_width_marg = int((width - (self.img_size * numb_nodes_row + margin_w * (numb_nodes_row - 1)))/2)

		# Calculating of size for current window size
		self.img_start = pygame.transform.scale(self.img_start_or, (self.img_size, self.img_size))
		self.img_end = pygame.transform.scale(self.img_end_or, (self.img_size, self.img_size))
		self.img_hub_norm = pygame.transform.scale(self.img_hub_norm_or, (self.img_size, self.img_size))
		self.img_hub_rest = pygame.transform.scale(self.img_hub_rest_or, (self.img_size, self.img_size))
		self.img_hub_prior = pygame.transform.scale(self.img_hub_prior_or, (self.img_size, self.img_size))
		self.img_hub_block = pygame.transform.scale(self.img_hub_block_or, (self.img_size, self.img_size))

		for node in self.node_map:

			norm_x = node.x - min_cord_x
			norm_y = node.y - min_cord_y

			start_screen_x = gen_width_marg + (margin_w * norm_x) + (self.img_size * norm_x)
			start_screen_y = gen_height_marg + (margin_h * norm_y) + (self.img_size * norm_y)

			node.rel_x = start_screen_x
			node.rel_y = start_screen_y

			node.center_x = start_screen_x + (self.img_size // 2)
			node.center_y = start_screen_y + (self.img_size // 2)
		
	def draw_menu(self, surface: pygame.Surface):
		surface.fill("teal")

		for con in self.node_map_holder.connections:
			pygame.draw.line(surface,
			                 "black",
							 (con.hub_s.center_x, con.hub_s.center_y),
							 (con.hub_e.center_x, con.hub_e.center_y))

		for node in self.node_map:
			if node == self.node_map_holder.start:
				current_img = self.img_start
			elif node == self.node_map_holder.end:
				current_img = self.img_end
			elif node.zone == ZoneType.BLOCKED:
				current_img = self.img_hub_block
			elif node.zone == ZoneType.PRIORITY:
				current_img = self.img_hub_prior
			elif node.zone == ZoneType.RESTRICTED:
				current_img = self.img_hub_rest
			else:
				current_img = self.img_hub_norm

			img_rect = current_img.get_rect(center=(node.center_x, node.center_y))

			surface.blit(current_img, img_rect)

			if node.color == "rainbow":
				text_surf = self.font.render(node.name, True, "green")
			else:
				text_surf = self.font.render(node.name, True, node.color)
			text_rect = text_surf.get_rect(midtop=(node.center_x, img_rect.bottom + 5))
			surface.blit(text_surf, text_rect)

