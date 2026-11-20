from .structures import Connection, Drone, Node, ZoneType
import pygame


class Schedule_drones():
	def __init__(self, ways: list[tuple[list[Connection], float]], numb_drons: int) -> None:
		self.all_ways: list[tuple[Connection, float]] = ways
		self.numb_drons: int = numb_drons
		self.schedule_drone: list[Drone] = []
		self.history: list[str] = []
		self.counter_steps: int = 0

	def get_price(self, hub: Node) -> int:
		if hub.zone == ZoneType.PRIORITY:
			return 1
		elif hub.zone == ZoneType.RESTRICTED:
			return 2
		else:
			return 1

	def fill_drones(self) -> None:
		for _ in range(self.numb_drons):
			self.schedule_drone.append(Drone())

	def check_drones(self) -> bool:
		for drone in self.schedule_drone:
			if not drone.finished:
				return False
		return True

	def take_shorter_pass(way: tuple[list[Connection], float] | None):
		pass

	def make_schedule(self) -> None:
		self.fill_drones()
		for drone in self.schedule_drone:
			pass
