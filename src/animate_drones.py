from .structures import Connection, Node
from .drone import Drone
import pygame


class Animate_drones():
	def __init__(self, schedule: list[list[tuple[Node | Connection, int]]], nb_drones: int, start: Node, end: Node):
		self.schedule: list[list[tuple[Node | Connection, int]]] = schedule
		self.nb_drones: int = nb_drones
		self.step: int = 1
		self.all_drones: list[Drone] = []
		self.start: Node = start
		self.end: Node = end
		self.final_step: int = 0
		self.counter_id: int = 0

	def update_metric_for_all_drones(self, width: int, height: int) -> None:
		for drone in self.all_drones:
			drone.update_metric(width, height, True)

	def create_new_drone(self) -> int:
		new_drone = Drone(self.counter_id, self.start.center_x, self.start.center_y, False, [self.start])
		if new_drone.init_all() == 1:
			return 1
		self.all_drones.append(new_drone)
		self.counter_id += 1
		return 0

	def check_drones(self) -> None:
		if not self.all_drones:
			return
		for drone in self.all_drones:
			if drone.finished:
				print(f"remove drone {drone.id}")
				self.all_drones.remove(drone)

	def	draw_drones(self, surface: pygame.Surface):
		for drone in self.all_drones:
			drone.draw(surface)

	def find_final_step(self) -> None:
		for way in self.schedule:
			for item in way:
				if item[1] > self.final_step:
					self.final_step = item[1]

	def start_animation(self, width: int, height: int) -> int:
		self.find_final_step()

		while self.step <= self.final_step:
			for i in range(self.nb_drones):
				for item in self.schedule[i]:
				# create drone when curent step eqval first step of this drone in schedule
					if (self.counter_id == i
						and self.step == item[1]):
						if self.create_new_drone() == 1:
							return 1
						self.update_metric_for_all_drones(width, height)

					if (self.step == item[1]
					    and self.all_drones):
						self.all_drones[i].take_target(item[0])
					
			self.step += 1
			self.check_drones()
		return 0






	