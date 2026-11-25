from .structures import Connection, Node
import pygame

class Drone:
	def __init__(self, id: int, x: int, y: int, finished: bool, position: Node):
		self.id: int = id
		self.x: int = x
		self.y: int = y
		self.center_x: int = 0
		self.center_y: int = 0
		self.finished: bool = finished
		self.position: Node | Connection = position
		self.target: Node | Connection = position
		self.img_drone_or: pygame.Surface | None = None
		self.img_drone: pygame.Syrface | None = None
		self.drone_size: int = 0

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
	
	def update_metric(self, width: int, height: int, its_first_time: bool):
		if its_first_time:
			self.x = self.position.center_x
			self.y = self.position.center_y
		base_w, base_h = 1280, 720
		scale = min(width / base_w, height / base_h)
		base_drone_size = 28
		self.drone_size = max(8, int(base_drone_size * scale))
		half = self.drone_size // 2
		self.center_x = half + self.x
		self.center_y = half + self.y
		print(f"{self.id} size - {self.drone_size}")
		self.finished = True

	def chek_in_target(self) -> bool:
		if ((self.center_x >= self.target.rel_x
		    and self.center_x <= (self.target.rel_x + self.target.size))
			or (self.center_y >= self.target.center_y
			and self.center_y <= (self.target.rel_y + self.target.size))):
			return True
		return False

	def take_target(self, target: Node | Connection) -> None:
		self.target = target
		print(self.target)

	def draw(self, surface: pygame.Surface) -> None:
		pass