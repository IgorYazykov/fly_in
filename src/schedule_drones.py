from .structures import Connection, Drone, Node, ZoneType
from functools import reduce
import pygame


class Schedule_drones():
	def __init__(self, ways: list[tuple[list[Connection], float]], numb_drons: int, start: Node, end: Node) -> None:
		self.all_ways: list[tuple[list[Connection], float]] = ways
		self.numb_drons: int = numb_drons
		self.start: Node = start
		self.end: Node = end
		self.drones: list[Drone] = []
		self.history: list[str] = []
		self.counter_steps: int = 0
		self.number_of_choice = 0

	def get_price(self, hub: Node) -> int:
		if hub.zone == ZoneType.PRIORITY:
			return 1
		elif hub.zone == ZoneType.RESTRICTED:
			return 2
		else:
			return 1

	def fill_drones(self) -> None:
		for i in range(self.numb_drons):
			self.drones.append(Drone(i,
									 self.start.center_x,
			                         self.start.center_y,
									 False,
									 [self.start]))

	def check_drones(self) -> bool:
		for drone in self.drones:
			if not drone.finished:
				return False
		return True

	def sorting_ways_by_price(self) -> None:
		self.all_ways.sort(key=lambda x: x[1])

	def check_node(self, drone: Drone, node: Node) -> bool:
		cur_cup = 0
		for elem in node.schedule:
			if elem[0] == len(drone.position):
				cur_cup += 1
		if cur_cup < node.max_drones:
			# print(f"go to node {node.name}")
			return True
		return False
		

	def try_to_take_connection(self, con: Connection, cur_step: int) -> bool:
		if con.max_link_capacity == None:
			return False
		if not con.schedule:
			# print(f"got to connection {con.hub_s.name}-{con.hub_e.name}")
			return True
		else:
			cur_cup = sum(1 for step, _ in con.schedule if step == cur_step)
			if cur_cup == con.max_link_capacity:
				return False
			# print(f"got to connection {con.hub_s.name}-{con.hub_e.name}")
			return True

	def wait_turn(self, curent_elem: int, drone: Drone) -> None:
		drone.position.append(drone.position[curent_elem - 1])
		drone.position[curent_elem - 1].schedule.append((len(drone.position), drone.id))


	def check_nod_in_ways(self, cur_price: float, cur_con: Connection) -> int:
		variants = []
		for i in range(len(self.all_ways)):
			if i != self.number_of_choice:
				for con in self.all_ways[i][0]:
					if (con.hub_s == cur_con.hub_s
					    and con.hub_e != cur_con.hub_e
						and self.all_ways[i][1] < (cur_price + 3)):
						variants.append((self.all_ways[i][1], i))

		if not variants:
			return -1

		variants.sort(key=lambda x: x[0])

		return variants[0][1]

	def take_decision(self,
	                  active_choice: tuple[list[Connection], float],
					  curent_elem: int,
					  drone: Drone) -> int:
		target = self.check_nod_in_ways(active_choice[1], active_choice[0][curent_elem])
		if target == -1:
			# stay on current hub
			# print(f"dron wait in{drone.position[curent_elem]}")
			self.wait_turn(len(drone.position), drone)
			return 0
		# print("switch way")
		self.number_of_choice = target
		return 0

	def try_to_make_step(self,
	                     active_choice: tuple[list[Connection], float],
						 curent_elem: int,
						 drone: Drone) -> int:
		# print(curent_elem)
		# print(len(active_choice[0]))
		if not active_choice[0][curent_elem].hub_e.schedule:
			active_choice[0][curent_elem].hub_e.schedule.append((len(drone.position), drone.id))
			drone.position.append(active_choice[0][curent_elem].hub_e)
			return 1
		else:
			# print("not easy way")
			if self.check_node(drone, active_choice[0][curent_elem].hub_e):
				active_choice[0][curent_elem].hub_e.schedule.append((len(drone.position), drone.id))
				drone.position.append(active_choice[0][curent_elem].hub_e)
				return 1
			else:
				if self.try_to_take_connection(active_choice[0][curent_elem], curent_elem):
					active_choice[0][curent_elem].schedule.append((len(drone.position), drone.id))
					drone.position.append(active_choice[0][curent_elem])
					return 0
				else:
					return self.take_decision(active_choice,  curent_elem, drone)

	def make_it_same_leng(self) -> None:
		max_leng = 0
		for drone in self.drones:
			len_pos = len(drone.position)
			if max_leng < len_pos:
				max_leng = len_pos

		for drone in self.drones:
			len_pos = len(drone.position)
			if len_pos < max_leng:
				dif = max_leng - len_pos
				for _ in range(dif):
					drone.position.append(drone.position[len_pos - 1])

	def make_schedule(self) -> None:
		self.fill_drones()
		self.sorting_ways_by_price()

		for drone in self.drones:
			curent_elem = 0
			self.number_of_choice = 0
			while not drone.finished and curent_elem < 50:
				active_choice = self.all_ways[self.number_of_choice]
				curent_elem += self.try_to_make_step(active_choice, curent_elem, drone)
				if (isinstance(drone.position[curent_elem], Node)
				    and drone.position[(len(drone.position) - 1)] == self.end):
					drone.finished = True

		self.make_it_same_leng()

		for i in range(len(self.drones[0].position)):
			for drone in self.drones:
				if isinstance(drone.position[i], Connection):
					print(f"D{drone.id} - {drone.position[i].hub_s.name}-{drone.position[i].hub_e.name}", end=" ")
				else:
					print(f"D{drone.id} - {drone.position[i].name}", end=" ")
			print("\n", end="")
		print("------------------------")
