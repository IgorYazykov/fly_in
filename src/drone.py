from .structures import Connection, Node
from typing import Any
import pygame

class Drone:
	def __init__(self, id: int, x: int, y: int, position: Node):
		self.id: int = id
		self.x: int = x
		self.y: int = y
		self.center_x: int = 0
		self.center_y: int = 0
		self.position: Node | Connection = position
		self.target: Node | Connection = position
		self.img_drone_or: pygame.Surface | None = None
		self.img_drone: pygame.Syrface | None = None
		self.drone_size: int = 0
		self.in_hub: bool = True
		self.have_target: bool = False
		self.pos_vector: pygame.Vector2 | None = None
		self.target_vector: pygame.Vector2 | None = None
		self.speed: int = 100

	def init_all(self) -> int:
		try:
			self.img_drone_or = pygame.image.load("src/img/drone.png")
		except pygame.error as err:
			print(err)
			return(1)
		except FileNotFoundError as err:
			print(err)
			return(1)
		return 0
	
	def update_metric(self, width: int, height: int):
		base_w, base_h = 1280, 720
		scale = min(width / base_w, height / base_h)
		base_drone_size = 100
		self.drone_size = max(8, int(base_drone_size * scale))
		if isinstance(self.target, Node):
			self.center_x = self.position.center_x
			self.center_y = self.position.center_y
		else:
			self.center_x = (self.position.hub_s.center_x + self.position.hub_e.center_x) // 2
			self.center_y = (self.position.hub_s.center_y + self.position.hub_e.center_y) // 2
		self.img_drone = pygame.transform.scale(self.img_drone_or, (self.drone_size, self.drone_size))
		if self.pos_vector == None:
			self.pos_vector = pygame.Vector2(float(self.center_x), float(self.center_y))
		if isinstance(self.target, Node):
			self.target_vector = pygame.Vector2(float(self.target.center_x), float(self.target.center_y))
		else:
			self.target_vector = pygame.Vector2(float((self.target.hub_s.center_x + self.target.hub_e.center_x) / 2),
			                                    float((self.target.hub_s.center_y + self.target.hub_e.center_y) / 2))

	def chek_in_target(self) -> bool:
		if self.pos_vector.distance_to(self.target_vector) <= 3.0:
			print(f"coord of drone = {self.pos_vector} and its target = {self.target_vector} and res is {self.pos_vector.distance_to(self.target_vector) <= 3.0}")
			self.position = self.target
			self.have_target = False
			return True
		return False

	def move_to_target(self, dt: Any) -> bool:
		if self.chek_in_target():
			# self.pos_vector = self.pos_vector.copy()
			return True
		self.pos_vector = self.pos_vector.move_towards(self.target_vector, self.speed * dt)
		return False
 
	def take_target(self, target: Node | Connection) -> None:
		self.target = target
		if isinstance(target, Node):
			print(f"target {target.name} for {self.id}")
			self.target_vector = pygame.Vector2(float(self.target.center_x), float(self.target.center_y))
		else:
			print(f"target {target.hub_s.name}-{target.hub_e.name} for {self.id}")
			self.target_vector = pygame.Vector2(float((self.target.hub_s.center_x + self.target.hub_e.center_x) / 2),
												float((self.target.hub_s.center_y + self.target.hub_e.center_y) / 2))
		self.have_target = True

	def draw(self, surface: pygame.Surface) -> None:
		half = self.drone_size // 2
		draw_pos = (int(self.pos_vector.x - half), int(self.pos_vector.y - half))
		surface.blit(self.img_drone, draw_pos)