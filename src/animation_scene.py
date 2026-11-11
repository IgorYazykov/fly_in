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

		numb_nodes_row = 0
		numb_nodes_col = 0
		x = []
		y = []
		if self.node_map_holder.connections[0].hub_s.x not in x:
			x.append(self.node_map_holder.connections[0].hub_s.x)
			numb_nodes_row += 1
		if self.node_map_holder.connections[0].hub_s.y not in y:
			y.append(self.node_map_holder.connections[0].hub_s.y)
			numb_nodes_col += 1
		for conect in self.node_map_holder.connections:
			if conect.hub_e.x not in x:
				x.append(conect.hub_e.x)
				numb_nodes_row += 1
			if conect.hub_e.y not in y:
				y.append(conect.hub_s.y)
				numb_nodes_col += 1

		print(numb_nodes_row, numb_nodes_col)

		border_h = int(height * 0.15)
		border_w = int(width * 0.12)

		min_margin = int(width * 0.05)

		size_node_w = int((width - (border_w * 2 + min_margin * (numb_nodes_row - 1))) / numb_nodes_row)
		size_node_h = int((height - (border_h * 2 + min_margin * (numb_nodes_row - 1))) / numb_nodes_col)
		
		img_size = int((size_node_h + size_node_w) / 2)

		# Calculating of size for current window size
		self.img_start = pygame.transform.scale(self.img_start, (img_size, img_size))
		self.img_end = pygame.transform.scale(self.img_end, (img_size, img_size))
		self.img_hub_norm = pygame.transform.scale(self.img_hub_norm, (img_size, img_size))
		self.img_hub_rest = pygame.transform.scale(self.img_hub_rest, (img_size, img_size))
		self.img_hub_prior = pygame.transform.scale(self.img_hub_prior, (img_size, img_size))
		self.img_hub_block = pygame.transform.scale(self.img_hub_block, (img_size, img_size))

		
	
	def draw_menu(self, surface: pygame.Surface):
		pass

