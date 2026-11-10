from .structures import Nodes_holder, Node, ZoneType
import pygame


class Animation():
	def __init__(self, node_map):
		self.node_map_holder: Nodes_holder  = node_map
		self.img_start: pygame.Surface | None = None
		self.img_end: pygame.Surface | None = None
		self.img_hub_norm: pygame.Surface | None = None
		self.img_hub_rest: pygame.Surface | None = None
		self.img_hub_prior: pygame.Surface | None = None
		self.img_hub_block: pygame.Surface | None = None
		self.font = None
		self.node_map: list[Node] = []

	def init_img(self) -> int:
		try:
			self.img_start = pygame.image.load("src/img/start-png-44879.png")
			self.img_end = pygame.image.load("src/img/finished-png-33595.png")
			self.img_hub_norm = pygame.image.load("src/img/square-png-25133.png")
			self.img_hub_rest = pygame.image.load("src/img/triangle-png-42421.png")
			self.img_hub_prior = pygame.image.load("src/img/circle-png-25307.png")
			self.img_hub_block = pygame.image.load("src/img/image.png")
			self.node_map = self.node_map_holder.nodes.copy()
			self.node_map.append(self.node_map_holder.start)
			self.node_map.append(self.node_map_holder.end)
			return(0)
		except pygame.error as err:
			print(err)
			return(1)
		
	def update_metric(self, width: int, height: int):
		self.font = pygame.font.SysFont("Arial", int(height * 0.025))

		img_size = int(height * 0.07)
		if img_size < 32:
			img_size = 32

		# Calculating of size for current window size
		self.img_start = pygame.transform.scale(self.img_start, (img_size, img_size))
		self.img_end = pygame.transform.scale(self.img_end, (img_size, img_size))
		self.img_hub_norm = pygame.transform.scale(self.img_hub_norm, (img_size, img_size))
		self.img_hub_rest = pygame.transform.scale(self.img_hub_rest, (img_size, img_size))
		self.img_hub_prior = pygame.transform.scale(self.img_hub_prior, (img_size, img_size))
		self.img_hub_block = pygame.transform.scale(self.img_hub_block, (img_size, img_size))

		xs = [node.x for node in self.node_map]
		xy = [node.y for node in self.node_map]
		min_x, min_y = min(xs), min(xy)
		max_x, max_y = max(xs), max(xy)

		range_x = max_x - min_x if max_x != min_x else 1
		range_y = max_y - min_y if max_y != min_y else 1

		padding_x = int(width * 0.15)
		padding_y = int(height * 0.2)
		draw_width = width - (padding_x * 2)
		draw_height = height - (padding_y * 2)

		for node in self.node_map:
			screen_x = padding_x + int(((node.x - min_x) / range_x) * draw_width)
			if max_y == min_y:
				screen_y = height // 2
			else:
				screen_y = padding_y = padding_y + int(((node.y - min_y) / range_y) * draw_height)

			node.x, node.y = screen_x, screen_y

	def draw_menu(self, surface: pygame.Surface):
		surface.fill((15, 15, 15))

		for conn in self.node_map_holder.connections:
			pygame.draw.line(surface, (100, 110, 130), (conn.hub_s.x, conn.hub_s.y), (conn.hub_e.x, conn.hub_e.y), width = 4)

		for node in self.node_map:
			print(node)
			if node == self.node_map_holder.start:
				current_img = self.img_start
			elif node == self.node_map_holder.end:
				current_img = self.img_end
			elif node.zone == ZoneType.NORMAL or node.zone == None:
				current_img = self.img_hub_norm
			elif node.zone == ZoneType.BLOCKED:
				current_img = self.img_hub_block
			elif node.zone == ZoneType.PRIORITY:
				current_img = self.img_hub_prior
			elif node.zone == ZoneType.RESTRICTED:
				current_img = self.img_hub_rest

			img_rect = current_img.get_rect(center=(node.x, node.y))

			surface.blit(current_img, img_rect)

			text_surf = self.font.render(node.name, True, (240, 240, 250))
			text_rect = text_surf.get_rect(center = (node.x, img_rect.top - 10))
			surface.blit(text_surf, text_rect)

