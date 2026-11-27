from .structures import Connection, Node
from .drone import Drone
from typing import Any
import pygame


class Animate_drones():
	def __init__(self, schedule: list[list[tuple[Node | Connection, int]]], nb_drones: int, start: Node, end: Node):
		self.schedule: list[list[tuple[Node | Connection, int]]] = schedule
		self.nb_drones: int = nb_drones
		# self.step: int = 1
		self.all_drones: list[Drone] = []
		self.start: Node = start
		self.end: Node = end
		self.final_step: int = 0
		self.counter_id: int = 0

	def update_metric_for_all_drones(self, width: int, height: int) -> None:
		for drone in self.all_drones:
			drone.update_metric(width, height)

	def create_new_drone(self) -> int:
		new_drone = Drone(self.counter_id,
		                  self.start.center_x,
						  self.start.center_y,
						  self.start)
		if new_drone.init_all() == 1:
			return 1
		self.all_drones.append(new_drone)
		self.counter_id += 1
		return 0

	def check_drones(self) -> None:
		if not self.all_drones:
			return
		for drone in self.all_drones:
			if drone.position == self.end:
				print(f"remove drone {drone.id}")
				self.all_drones.remove(drone)

	def	draw_drones(self, surface: pygame.Surface):
		for drone in self.all_drones:
			drone.draw(surface)

	def find_final_step(self) -> None:
		print(self.schedule)
		for way in self.schedule:
			for item in way:
				if item[1] > self.final_step:
					self.final_step = item[1]

	def take_targets(self, id, step) -> Node | Connection | None:
		for target, target_step in self.schedule[id]:
			if target_step == step:
				return target
		return None

	def drones_handeler(self, width: int, height: int, step: int, dt: Any) -> int:
		for id in range(self.counter_id, self.nb_drones):
			if self.take_targets(id, step) != None:
				if self.create_new_drone() == 1:
					return -1
				self.update_metric_for_all_drones(width, height)

		for drone in self.all_drones:
			if not drone.have_target:
				target = self.take_targets(drone.id, step)
				if not target == None:
					drone.take_target(target)

		counter_drones_in_target = 0
		for drone in self.all_drones:
			if drone.move_to_target(dt):
				counter_drones_in_target += 1

		self.check_drones()

		if self.all_drones and counter_drones_in_target == len(self.all_drones):
			return 1
		return 0
	