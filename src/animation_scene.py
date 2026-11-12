from .structures import Nodes_holder, Node, ZoneType
import pygame


class Animation():
	def __init__(self, node_map):
		self.node_map_holder: Nodes_holder = node_map
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
		self.font_size = int(height * 0.025)
		self.font = pygame.font.SysFont("Arial", self.font_size)

		numb_nodes_row = 1
		numb_nodes_col = 1

		min_cord_x = min(self.node_map, key=lambda node: node.x).x
		min_cord_y = min(self.node_map, key=lambda node: node.y).y
		max_cord_x = max(self.node_map, key=lambda node: node.x).x
		max_cord_y = max(self.node_map, key=lambda node: node.y).y

		if min_cord_x > 0:
			numb_nodes_row += max_cord_x - min_cord_x
		elif min_cord_x < 0:
			min_cord_x *= -1
			numb_nodes_row += min_cord_x + max_cord_x
		else:
			numb_nodes_row += max_cord_x

		if min_cord_y > 0:
			numb_nodes_col += max_cord_y - min_cord_y
		elif min_cord_y < 0:
			min_cord_y *= -1
			numb_nodes_col += min_cord_y + max_cord_y
		else:
			numb_nodes_col += max_cord_y

		border_h = int(height * 0.15)
		border_w = int(width * 0.12)

		min_margin = int(width * 0.05)

		size_node_w = int((width - (border_w * 2 + min_margin * (numb_nodes_row - 1))) / numb_nodes_row)
		size_node_h = int((height - (border_h * 2 + min_margin * (numb_nodes_col - 1))) / numb_nodes_col)
		
		self.img_size = min(size_node_h, size_node_w)

		# Calculating of size for current window size
		self.img_start = pygame.transform.scale(self.img_start, (self.img_size, self.img_size))
		self.img_end = pygame.transform.scale(self.img_end, (self.img_size, self.img_size))
		self.img_hub_norm = pygame.transform.scale(self.img_hub_norm, (self.img_size, self.img_size))
		self.img_hub_rest = pygame.transform.scale(self.img_hub_rest, (self.img_size, self.img_size))
		self.img_hub_prior = pygame.transform.scale(self.img_hub_prior, (self.img_size, self.img_size))
		self.img_hub_block = pygame.transform.scale(self.img_hub_block, (self.img_size, self.img_size))

		cord_up_x = min(self.node_map, key=lambda node: node.x).x
		cord_up_y = min(self.node_map, key=lambda node: node.y).y
		if cord_up_x < 0:
			hub_names = []
			cord_up_x *= -1
			self.node_map_holder.connections[0].hub_s.x += cord_up_x
			hub_names.append(self.node_map_holder.connections[0].hub_s.name)
			for con in self.node_map_holder.connections:
				if con.hub_e.name not in hub_names:
					con.hub_e.x += cord_up_x
					hub_names.append(con.hub_e.name)
		if cord_up_y < 0:
			hub_names = []
			cord_up_y *= -1
			self.node_map_holder.connections[0].hub_s.y += cord_up_y
			hub_names.append(self.node_map_holder.connections[0].hub_s.name)
			for con in self.node_map_holder.connections:
				if con.hub_e.name not in hub_names:
					con.hub_e.y += cord_up_y
					hub_names.append(con.hub_e.name)

		self.node_map_holder.connections[0].hub_s.rel_x = (
			(self.node_map_holder.connections[0].hub_s.x * self.img_size)
			+ (border_w)
			+ (self.node_map_holder.connections[0].hub_s.x * min_margin)
		)
		self.node_map_holder.connections[0].hub_s.center_x = (
			self.node_map_holder.connections[0].hub_s.rel_x + (self.img_size//2)
		)
		self.node_map_holder.connections[0].hub_s.rel_y = (
			(self.node_map_holder.connections[0].hub_s.y * self.img_size)
			+ (border_h)
			+ (self.node_map_holder.connections[0].hub_s.y * min_margin)
		)
		self.node_map_holder.connections[0].hub_s.center_y = (
			self.node_map_holder.connections[0].hub_s.rel_y + (self.img_size//2)
		)
		hub_names = []
		for con in self.node_map_holder.connections:
			if con.hub_e.name not in hub_names:
				con.hub_e.rel_x = (
					(con.hub_e.x * self.img_size)
					+ (border_w)
					+ (con.hub_e.x * min_margin)
				)
				con.hub_e.center_x = con.hub_e.rel_x + (self.img_size//2)
				con.hub_e.rel_y = (
					(con.hub_e.y * self.img_size)
					+ (border_h)
					+ (con.hub_e.y * min_margin)
				)
				con.hub_e.center_y = con.hub_e.rel_y + (self.img_size//2)
				hub_names.append(con.hub_e.name)
		
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

			text_surf = self.font.render(node.name, True, node.color)
			text_rect = text_surf.get_rect(center=(
				(node.rel_x + (self.img_size//2)) - self.font_size,
				node.rel_y + self.img_size + self.font_size))
			surface.blit(text_surf, text_rect)

